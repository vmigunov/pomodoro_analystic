from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1848930ee6da"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаем таблицу Categories
    op.create_table(
        "Categories",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("category_name", sa.String),
        # Добавьте другие колонки Categories по необходимости
    )

    # Создаем таблицу Tasks
    op.create_table(
        "Tasks",
        sa.Column(
            "id", sa.Integer, primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("pomodoro_count", sa.INTEGER),
        sa.Column("category_id", sa.String),
        # Добавьте другие колонки Tasks по необходимости
    )

    # Создаем foreign key (если нужно)
    op.create_foreign_key(
        "fk_tasks_category_id", "Tasks", "Categories", ["category_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем таблицы в обратном порядке
    op.drop_table("Tasks")
    op.drop_table("Categories")
