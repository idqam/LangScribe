from Persistence.DTOs import ReportCreate, ReportUpdate
from Persistence.Models import Language, Report, User
from Resources import transaction
from sqlalchemy import delete, select, update


async def get_all_reports() -> list[Report]:
    async with transaction() as session:
        res = await session.execute(
            select(Report),
        )

        reports: list[Report] = res.scalars().all()

    return reports


async def get_one_report(tmp_id: int | None) -> Report:
    async with transaction() as session:

        report = await session.execute(
            select(Report).where(Report.id == tmp_id),
        )

        if not report.scalar_one_or_none():
            raise ValueError("Report not found")

    return report.scalar_one_or_none()


async def update_report(tmp_id: int, tmp_report: ReportUpdate) -> Report:
    async with transaction() as session:

        report = await session.get(Report, tmp_id)

        if not report:
            raise ValueError("Report not found")

        res = await session.execute(
            update(Report).where(Report.id == tmp_id).values(**tmp_report.model_dump(exclude_unset=True)),
        )

        if res.rowcount == 0:
            raise ValueError("Update failed - no rows affected")

    return res.rowcount


async def create_report(tmp_report: ReportCreate) -> Report:
    async with transaction() as session:

        user = await session.get(User,tmp_report.user_id)
        language = await session.get(Language,tmp_report.language_id)

        if not user or not language:
            raise ValueError("user or language not found!")

        new_report = Report(**tmp_report.model_dump())
        session.add(new_report)
        await session.flush()
        await session.refresh(new_report)

    return new_report


async def delete_report(id: int) -> int:
    async with transaction() as session:
        report = await session.get(Report,id)

        if not report:
            raise ValueError("Report not found")

        res = await session.execute(
            delete(Report).where(Report.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")

        count: int = res.rowcount
    return count
