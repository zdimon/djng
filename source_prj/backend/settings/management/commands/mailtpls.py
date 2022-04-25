from settings.models import MailTemplates


def load_mail_tpls():
    MailTemplates.objects.all().delete()
    m = MailTemplates()
    m.alias = 'man-registration'
    m.title = 'Man registartion'
    m.title_ru = 'Регистрация мужчины'
    m.content_en = 'Your password is {password}'
    m.content_ru = 'Ваш пароль {password}'
    m.save()

    m = MailTemplates()
    m.alias = 'password-reset'
    m.title = 'Password reset'
    m.title_ru = 'Сброс пароля'
    m.content_en = 'Link {reset_password_url}'
    m.content_ru = 'Ссылка {reset_password_url}'
    m.save()

    m = MailTemplates()
    m.alias = 'woman-registration'
    m.title = 'Woman registartion'
    m.title_ru = 'Регистрация женщины'
    m.content_en = 'Your password is {password}'
    m.content_ru = 'Ваш пароль {password}'
    m.save()
