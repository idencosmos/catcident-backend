# homepage/models/global_models.py
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class SiteTitle(TranslatableModel):
    translations = TranslatedFields(title=models.CharField(max_length=200))

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or "SiteTitle"

    class Meta:
        verbose_name = "G01. Site Title"
        verbose_name_plural = "G01. Site Titles"


class NavigationGroup(TranslatableModel):
    highlighted = models.BooleanField(default=False)

    translations = TranslatedFields(group_label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("group_label", any_language=True)
            or f"Group {self.pk}"
        )

    class Meta:
        verbose_name = "G02. Navigation Group"
        verbose_name_plural = "G02. Navigation Groups"


class NavigationSubMenu(TranslatableModel):
    parent_group = models.ForeignKey(
        NavigationGroup, related_name="sub_menus", on_delete=models.CASCADE
    )
    href = models.CharField(max_length=200)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"SubMenu {self.pk}"
        )

    class Meta:
        verbose_name = "G03. Navigation SubMenu"
        verbose_name_plural = "G03. Navigation SubMenus"


class FooterSection(TranslatableModel):
    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"Footer {self.pk}"
        )

    class Meta:
        verbose_name = "G04. Footer Section"
        verbose_name_plural = "G04. Footer Sections"


class FooterSubMenu(TranslatableModel):
    footer_section = models.ForeignKey(
        FooterSection, related_name="sub_menus", on_delete=models.CASCADE
    )
    href = models.CharField(max_length=200)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"FooterSubMenu {self.pk}"
        )

    class Meta:
        verbose_name = "G05. Footer SubMenu"
        verbose_name_plural = "G05. Footer SubMenus"


class FamilySite(TranslatableModel):
    href = models.CharField(max_length=200)

    translations = TranslatedFields(label=models.CharField(max_length=100))

    def __str__(self):
        return (
            self.safe_translation_getter("label", any_language=True)
            or f"FamilySite {self.pk}"
        )

    class Meta:
        verbose_name = "G06. Family Site"
        verbose_name_plural = "G06. Family Sites"


class Copyright(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Copyright"

    class Meta:
        verbose_name = "G07. Copyright"
        verbose_name_plural = "G07. Copyright"
