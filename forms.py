from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email


DATA_REQUIRED_ERR_MSG = 'Это поле не может быть пустым'


class PhoneValidator(Length):
    def __call__(self, form, field):
        super().__call__(form, field)
        if not field.data[1:].isdigit() or not (field.data[0] == '+' or field.data[0].isdigit()):
            message = self.message
            if message is None:
                message = field.gettext('Телефон может содержать только цифры и начинаться со знака + или цифры')
            raise ValidationError(message)


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [DataRequired(DATA_REQUIRED_ERR_MSG)])
    address = StringField('Адрес', [DataRequired(DATA_REQUIRED_ERR_MSG)])
    email = StringField('Электронная почта', [DataRequired(DATA_REQUIRED_ERR_MSG), Email()])
    phone = StringField('Ваш телефон', [DataRequired(DATA_REQUIRED_ERR_MSG), PhoneValidator(min=11, max=12)])
    submit = SubmitField('Отправить заказ')


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', [DataRequired(DATA_REQUIRED_ERR_MSG), Email()])
    password = PasswordField('Пароль', [DataRequired(DATA_REQUIRED_ERR_MSG)])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Электронная почта', [DataRequired(DATA_REQUIRED_ERR_MSG), Email()])
    password = PasswordField(
        'Пароль',
        [
            DataRequired(DATA_REQUIRED_ERR_MSG), Length(min=5, message="Пароль должен быть не менее 5 символов"),
            EqualTo('confirm_password', message='Пароли не сопадают')
        ])
    confirm_password = PasswordField(
        'Повторите пароль',
        [DataRequired(DATA_REQUIRED_ERR_MSG), Length(min=5, message="Пароль должен быть не менее 5 символов")]
    )
    submit = SubmitField('Зарегистрироваться')
