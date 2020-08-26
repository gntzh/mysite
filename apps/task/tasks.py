from celery import task

from .check import Check

check = Check('sure.z@outlook.com')

@task
def check_task(username, password, email=None):
    session = check.make_session()
    status, _ = check.login(session, username, password)
    if not status:
        check.inform(
            email or check.email,
            check.email_subject_tpl.format(username=username, event="登录", status="失败"),
            check.email_content_tpl.format(detail=_),
        )
        return
    email = email or _ or check.email
    status, _ = check.log(session)
    if not status:
        check.inform(
            email,
            check.email_subject_tpl.format(username=username, event="Log", status="失败"),
            check.email_content_tpl.format(detail=_),
        )
    check_status, _ = check.check_status(session)
    if check_status is None:
        check.inform(
            email,
            check.email_subject_tpl.format(
                username=username, event="Check状态请求", status="失败"
            ),
            check.email_content_tpl.format(detail=_),
        )
    elif not check_status:
        status, _ = check.check(session)
        check_status, __ = check.check_status(session)
        check.inform(
            email,
            check.email_subject_tpl.format(
                username=username,
                event="Check",
                status="成功" if status and check_status else "失败",
            ),
            check.email_content_tpl.format(detail=_ + "\n" + _, code=""),
        )
    else:
        check.inform(
            email,
            check.email_subject_tpl.format(
                username=username, event="Check手动", status="成功",
            ),
            check.email_content_tpl.format(detail="检测到已经完成", code=""),
        )
