import csv
import io
import re
from datetime import date

from sqlalchemy.orm import Session

from app.repositories.account import AccountRepository
from app.repositories.category import CategoryRepository
from app.repositories.category_rule import CategoryRuleRepository
from app.repositories.transaction import TransactionRepository
from app.schemas.transaction import (
    ImportResult,
    TransactionCreate,
    TransactionListResponse,
    TransactionOut,
    TransactionUpdate,
)

# Map CSV account names to account_type
ACCOUNT_TYPE_MAP = {
    "checking": "checking",
    "savings": "savings",
    "credit": "credit_card",
    "venture": "credit_card",
    "quicksilver": "credit_card",
    "platinum": "credit_card",
    "blue cash": "credit_card",
    "ira": "ira",
    "brokerage": "brokerage",
    "401k": "401k",
    "mortgage": "mortgage",
    "loan": "loan",
}


def _guess_account_type(account_name: str) -> str:
    name_lower = account_name.lower()
    for keyword, acct_type in ACCOUNT_TYPE_MAP.items():
        if keyword in name_lower:
            return acct_type
    return "other"


def _parse_amount(amount_str: str) -> float:
    """Parse amount strings like '-$1,697.09' or '$5,700.00'."""
    cleaned = amount_str.replace("$", "").replace(",", "").strip()
    return float(cleaned)


def _extract_last_four(account_name: str) -> str | None:
    """Extract last 4 digits from account name like 'Ending in 2820'."""
    match = re.search(r"Ending in (\w+)", account_name)
    if match:
        return match.group(1)[-4:]
    return None


def _clean_account_name(account_name: str) -> str:
    """Clean the account name — remove the 'Ending in XXXX' suffix."""
    match = re.match(r"^(.+?)\s*-?\s*Ending in \w+$", account_name)
    if match:
        return match.group(1).strip()
    return account_name.strip()


class TransactionService:
    def __init__(self, db: Session):
        self.txn_repo = TransactionRepository(db)
        self.account_repo = AccountRepository(db)
        self.category_repo = CategoryRepository(db)
        self.rule_repo = CategoryRuleRepository(db)

    def list_transactions(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "date",
        sort_dir: str = "desc",
        account_id: int | None = None,
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> TransactionListResponse:
        items, total = self.txn_repo.list(
            page=page,
            page_size=page_size,
            q=q,
            sort_by=sort_by,
            sort_dir=sort_dir,
            account_id=account_id,
            category_id=category_id,
            date_from=date_from,
            date_to=date_to,
        )
        return TransactionListResponse(
            items=[TransactionOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_transaction(self, data: TransactionCreate) -> TransactionOut:
        txn = self.txn_repo.create(
            date=data.date,
            description=data.description,
            amount=data.amount,
            category_id=data.category_id,
            account_id=data.account_id,
            tags=data.tags,
            notes=data.notes,
        )
        return TransactionOut.model_validate(txn)

    def update_transaction(self, txn_id: int, data: TransactionUpdate) -> TransactionOut | None:
        update_data = data.model_dump(exclude_unset=True)
        txn = self.txn_repo.update(txn_id, **update_data)
        if not txn:
            return None

        # If category was changed, learn a rule from it
        if data.category_id is not None:
            self._learn_category_rule(txn.description, data.category_id)

        return TransactionOut.model_validate(txn)

    def delete_transaction(self, txn_id: int) -> bool:
        return self.txn_repo.delete(txn_id)

    def import_csv(self, csv_content: str) -> ImportResult:
        """Import transactions from CSV content matching the expected format."""
        reader = csv.DictReader(io.StringIO(csv_content))
        imported = 0
        skipped = 0
        accounts_created_set: set[str] = set()
        categories_created_set: set[str] = set()

        rows = list(reader)
        for row in rows:
            try:
                txn_date = date.fromisoformat(row["Date"])
                description = row["Description"].strip()
                raw_description = description
                amount = _parse_amount(row["Amount"])
                category_name = row.get("Category", "").strip()
                firm_name = row.get("Firm Name", "").strip()
                account_name_raw = row.get("Account Name", "").strip()
                tags = row.get("Tags", "").strip() or None

                # Get or create account
                account_id = None
                if account_name_raw and firm_name:
                    clean_name = _clean_account_name(account_name_raw)
                    account = self.account_repo.find_by_name_and_institution(clean_name, firm_name)
                    if not account:
                        last_four = _extract_last_four(account_name_raw)
                        account = self.account_repo.create(
                            name=clean_name,
                            institution=firm_name,
                            account_type=_guess_account_type(account_name_raw),
                            last_four=last_four,
                        )
                        accounts_created_set.add(clean_name)
                    account_id = account.id

                # Get or create category
                category_id = None
                if category_name:
                    category = self.category_repo.get_or_create(category_name, is_system=True)
                    if category.name in categories_created_set or not category.is_system:
                        pass  # already counted
                    categories_created_set.add(category.name)
                    category_id = category.id

                self.txn_repo.create(
                    date=txn_date,
                    description=description,
                    raw_description=raw_description,
                    amount=amount,
                    category_id=category_id,
                    account_id=account_id,
                    tags=tags,
                )
                imported += 1
            except (KeyError, ValueError):
                skipped += 1

        return ImportResult(
            imported=imported,
            skipped=skipped,
            accounts_created=len(accounts_created_set),
            categories_created=len(categories_created_set),
        )

    def _learn_category_rule(self, description: str, category_id: int) -> None:
        """Create a category rule from a user's manual categorization."""
        existing = self.rule_repo.find_matching(description)
        if existing and existing.category_id == category_id:
            self.rule_repo.increment_applied(existing.id)
            return
        # Create new rule using the full description as pattern
        self.rule_repo.create(
            pattern=description.lower(),
            category_id=category_id,
            confidence=0.8,
        )
