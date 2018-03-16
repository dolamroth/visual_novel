from rest_framework import serializers

from django.conf import settings

from cinfo.models import Studio, StaffRole, Staff, Tag, Genre
from vn_core.models import VisualNovel, VNStaff, VNStudio, VNTag, VNGenre


class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ('title', )


class StaffSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    title = serializers.CharField()

    class Meta:
        model = Staff
        fields = ('roles', 'title')

    def get_roles(self, obj):
        vnstaffs = VNStaff.objects.filter(staff=obj).order_by('-weight')
        roles = [vnstaffs[i].role for i in range(len(vnstaffs))]
        serializer = StaffRoleSerializer(roles, many=True)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'description')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title', 'description')


class StudioSerializers(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, style={'base_template': 'textarea.html'})

    class Meta:
        model = Studio
        fields = ('title', 'description')


class VisualNovelSerializer(serializers.ModelSerializer):

    studios = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    longevity = serializers.CharField(source='longevity.__str__')

    class Meta:
        model = VisualNovel
        fields = ('title', 'description', 'studios', 'photo', 'staff', 'genres', 'tags', 'date_of_release',
                  'vndb_id', 'steam_link', 'longevity')

    def get_staff(self, obj):
        staffs = obj.staff.all().distinct('title')
        return StaffSerializer(staffs, many=True).data

    def get_studios(self, obj):
        vnstudios = VNStudio.objects.filter(visual_novel=obj).order_by('-weight')
        studios = [vnstudios[i].studio for i in range(len(vnstudios))]
        return StudioSerializers(studios, many=True).data

    def get_genres(self, obj):
        vngenres = VNGenre.objects.filter(visual_novel=obj).order_by('-weight')
        genres = [vngenres[i].genre for i in range(len(vngenres))]
        return GenreSerializer(genres, many=True).data

    def get_tags(self, obj):
        vntags = VNTag.objects.filter(visual_novel=obj).order_by('-weight')
        tags = [vntags[i].tag for i in range(len(vntags))]
        return TagSerializer(tags, many=True).data

    def get_photo(self, obj):
        if not obj.photo:
            return settings.POSTER_STOPPER_URL
        return obj.photo.url
