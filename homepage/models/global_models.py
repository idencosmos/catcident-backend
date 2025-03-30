# homepage/models/global_models.py
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class SiteTitle(TranslatableModel):
    translations = TranslatedFields(title=models.CharField(max_length=200))

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or "SiteTitle"

    class Meta:
        verbose_name = "_01. Site Title"
        verbose_name_plural = "_01. Site Titles"


class NavigationGroup(TranslatableModel):
    highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    translations = TranslatedFields(group_label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("group_label", any_language=True)
            or f"Group {self.pk}"
        )

    class Meta:
        verbose_name = "_02. Navigation Group"
        verbose_name_plural = "_02. Navigation Groups"
        ordering = ["order"]


class NavigationSubMenu(TranslatableModel):
    parent_group = models.ForeignKey(
        NavigationGroup, related_name="sub_menus", on_delete=models.CASCADE
    )
    href = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"SubMenu {self.pk}"
        )

    class Meta:
        verbose_name = "Navigation SubMenu"
        verbose_name_plural = "Navigation SubMenus"
        ordering = ["order"]


class FooterSection(TranslatableModel):
    translations = TranslatedFields(label=models.CharField(max_length=100))
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"Footer {self.pk}"
        )

    class Meta:
        verbose_name = "_03. Footer Section"
        verbose_name_plural = "_03. Footer Sections"
        ordering = ["order"]


class FooterSubMenu(TranslatableModel):
    footer_section = models.ForeignKey(
        FooterSection, related_name="sub_menus", on_delete=models.CASCADE
    )
    href = models.CharField(max_length=200)
    open_in_new_tab = models.BooleanField(default=False, verbose_name="새 창에서 열기")
    order = models.PositiveIntegerField(default=0)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"FooterSubMenu {self.pk}"
        )

    class Meta:
        verbose_name = "Footer SubMenu"
        verbose_name_plural = "Footer SubMenus"
        ordering = ["order"]


class FamilySite(TranslatableModel):
    href = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"FamilySite {self.pk}"
        )

    class Meta:
        verbose_name = "_04. Family Site"
        verbose_name_plural = "_04. Family Sites"
        ordering = ["order"]


class Copyright(models.Model):
    text = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Copyright"

    class Meta:
        verbose_name = "_05. Copyright"
        verbose_name_plural = "_05. Copyright"
