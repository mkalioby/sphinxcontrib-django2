from django.db import models

try:
    from phonenumber_field.modelfields import PhoneNumberField

    PHONENUMBER = True
except ModuleNotFoundError:
    # In case phonenumber is not used, pass
    PHONENUMBER = False


class SimpleModelManager(models.Manager):
    pass


class FileModel(models.Model):
    upload = models.FileField()


class SimpleModel(models.Model):
    # Foreign Keys
    file = models.ForeignKey(
        "FileModel",
        related_name="simple_models",
        on_delete=models.CASCADE,
    )

    # One to one field
    childA = models.OneToOneField(
        "ChildModelA",
        related_name="simple_model",
        on_delete=models.CASCADE,
    )

    # Many to many field
    childrenB = models.ManyToManyField(
        "ChildModelB",
        related_name="simple_models",
    )

    # Dummy field
    dummy_field = models.CharField(
        max_length=3,
        help_text="This should help you",
        verbose_name="Very verbose name of dummy field",
    )

    #: Custom model manager
    custom_objects = SimpleModelManager()

    # Mock get_..._display method of Django models
    def get_dummy_field_display(self):
        pass

    # Mock common get_next_by_ method
    def get_next_by_dummy_field(self):
        pass

    # Mock common get_previous_by_ method
    def get_previous_by_dummy_field(self):
        pass


class AbstractModel(models.Model):
    simple_model = models.ForeignKey(
        "SimpleModel",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey("auth.User", related_name="+", on_delete=models.CASCADE)
    foreignkey_self = models.ForeignKey("self", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ChildModelA(AbstractModel):
    pass


class ChildModelB(AbstractModel):
    pass


if PHONENUMBER:

    class PhoneNumberModel(models.Model):
        phone_number = PhoneNumberField()
