from django.contrib import admin
from .models import Mission, MercenaryProfile, NewsCards,Customer

# ثبت مدل Mission
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date')
    search_fields = ('title', 'location')
    list_filter = ('date',)
    ordering = ('-date',)
    list_per_page = 25

# ثبت مدل Mercenary
@admin.register(MercenaryProfile)
class MercenaryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'military_specialty',
        'military_rank',
        'nationality',
        'battalion',
        'age'
    )
    search_fields = ('name', 'military_specialty', 'military_rank', 'nationality')
    list_filter = ('nationality', 'military_rank', 'battalion')
    ordering = ('-age',)
    list_per_page = 25

# ثبت مدل CustomerAlias
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['alias', 'created_at']

# ثبت مدل NewsCards
@admin.register(NewsCards)
class NewsCardsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'enabled')
    list_editable = ('enabled',)
    search_fields = ('site_name',)
