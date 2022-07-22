from django.conf import settings
from django.db.models import Exists, OuterRef, QuerySet, Prefetch, Subquery

from constance import config

from chart.models import ChartItemToUser, ChartItem, ChartItemTranslator, ChartRating
from chart.serializers import ChartItemListSerializer
from cinfo.genres.models import Genre
from cinfo.longevity.models import Longevity
from cinfo.staffs.models import Staff
from cinfo.studios.models import Studio
from cinfo.tags.models import Tag
from cinfo.translators.models import Translator
from vn_core.models import VNGenre, VNTag, VNStudio, VNStaff


class ChartViewContext:
	max_vn_by_row = settings.CHART_NUMBER_OF_VN_IN_ROW

	base_sort_by = '-date_of_translation'

	# These two arrays are coordinated in terms of order of elements and corresponding data
	# This array shows all the possible GET parameters for "sort"
	all_sortings = ['-date_of_translation', 'date_of_translation', 'visual_novel__rate', '-visual_novel__rate',
	                '-visual_novel__date_of_release', 'visual_novel__date_of_release', '-visual_novel__title',
	                'visual_novel__title', 'visual_novel__popularity', '-visual_novel__popularity']
	# This array provides alternative sorting for one selected parameter, which is chosen by user,
	# and a title of glyphoicon from Bootstrap
	all_sortings_context_links = [
		('date_of_translation', 'date_of_translation', 'glyphicon glyphicon-arrow-down'),
		('date_of_translation', '-date_of_translation', 'glyphicon glyphicon-arrow-up'),
		('rate', '-visual_novel__rate', 'glyphicon glyphicon-arrow-up'),
		('rate', 'visual_novel__rate', 'glyphicon glyphicon-arrow-down'),
		('date_of_release', 'visual_novel__date_of_release', 'glyphicon glyphicon-arrow-down'),
		('date_of_release', '-visual_novel__date_of_release', 'glyphicon glyphicon-arrow-up'),
		('title', 'visual_novel__title', 'glyphicon glyphicon-arrow-down'),
		('title', '-visual_novel__title', 'glyphicon glyphicon-arrow-up'),
		('popularity', '-visual_novel__popularity', 'glyphicon glyphicon-arrow-up'),
		('popularity', 'visual_novel__popularity', 'glyphicon glyphicon-arrow-down'),
	]

	def __init__(
			self, request, additional_breadcumb, title, genre_alias = None, tag_alias = None, studio_alias = None,
			staff_alias = None, duration_alias = None, translator_alias = None,
	):
		self.title = title
		self.additional_breadcumb = additional_breadcumb
		self.all_chart_items = self.init_chart_items(request=request, page=additional_breadcumb)
		self.context = {}

		# Sorting list of visual novels
		self.sort_by_str = request.GET.get('sort')

		self.chart_breadcumb_with_link = f'&nbsp;&#47; <a href="/chart/">{additional_breadcumb}</a>&nbsp;&#47; '

		self.sort(genre_alias=genre_alias, tag_alias=tag_alias, studio_alias=studio_alias,
		          staff_alias=staff_alias, duration_alias=duration_alias, translator_alias=translator_alias)

		self.rows = []

		self.serialize()

	def get_context(self) -> dict:
		if not self.context.get('additional_breadcumb'):
			self.context['additional_breadcumb'] = f'&nbsp;&#47; {self.additional_breadcumb}'
		if not self.context.get('additional_description'):
			self.context['additional_description'] = ''

		self.context['all_genres'] = Genre.objects.filter(is_published=True).order_by('title')
		self.context['all_tags'] = Tag.objects.filter(is_published=True).order_by('title')
		self.context['all_durations'] = Longevity.objects.filter(is_published=True).order_by('max_length')
		self.context['all_studios'] = Studio.objects.filter(is_published=True).order_by('title')
		self.context['all_staff'] = Staff.objects.filter(is_published=True).order_by('title')

		# This is base data for providing icons and links, in case nothing is selected by user
		self.context['date_of_translation'] = '-date_of_translation'
		self.context['date_of_translation_icon'] = 'glyphicon glyphicon-arrow-down'
		self.context['rate'] = '-visual_novel__rate'
		self.context['rate_icon'] = ''
		self.context['date_of_release'] = '-visual_novel__date_of_release'
		self.context['date_of_release_icon'] = ''
		self.context['title'] = self.title
		self.context['title_icon'] = ''
		self.context['popularity'] = '-visual_novel__popularity'
		self.context['popularity_icon'] = ''
		self.context['base_poster_url'] = config.CHART_POSTER_NOT_LOADED_IMAGE or settings.POSTER_STOPPER_URL

		self.context['stars_count'] = [n for n in range(1, 11)]

		self.context['rows'] = self.rows
		self.context['no_rows'] = (len(self.context['rows']) == 0)
		if self.context['no_rows']:
			self.context['additional_breadcumb'] = f'&nbsp;&#47;&nbsp;<a href="/chart/">{self.additional_breadcumb}</a>'

		return self.context

	def init_chart_items(self, request, page) -> QuerySet:
		all_charts = ChartItem.objects.select_related('visual_novel')
		if not request.user.is_authenticated:
			return all_charts

		user_favorites_charts = ChartItemToUser.objects.filter(user=request.user, chart_item_id=OuterRef('id'))
		user_rated_charts = ChartRating.objects.filter(user=request.user, chart_item_id=OuterRef('id'))

		chart_rating_subquery = ChartRating.objects.filter(chart_item_id=OuterRef('id'), user=request.user) \
			                        .values('rating')[:1]

		all_charts = ChartItem.objects.select_related('visual_novel') \
			.filter(is_published=True, visual_novel__is_published=True) \
			.annotate(is_favorite=Exists(user_favorites_charts)) \
			.annotate(is_rated=Exists(user_rated_charts)) \
			.annotate(user_rating=Subquery(chart_rating_subquery))

		if page == 'Чарт':
			return all_charts
		elif page == 'Избранное':
			return all_charts.filter(is_favorite=True)

	def sort(self, genre_alias = None, tag_alias = None, studio_alias = None,
	         staff_alias = None, duration_alias = None, translator_alias = None):
		if genre_alias:
			self.sort_by(
				vn_model=VNGenre,
				model=Genre,
				lookup={'genre__alias': genre_alias},
				alias=genre_alias,
				value='жанр'
			)
		if tag_alias:
			self.sort_by(
				vn_model=VNTag,
				model=Tag,
				lookup={'tag__alias': tag_alias},
				alias=tag_alias,
				value='тег'
			)
		if studio_alias:
			self.sort_by(
				vn_model=VNStudio,
				model=Studio,
				lookup={'studio__alias': studio_alias},
				alias=studio_alias,
				value='студия'
			)
		if staff_alias:
			self.sort_by_staff(staff_alias=staff_alias)
		if duration_alias:
			self.sort_by_duration(duration_alias=duration_alias)
		if translator_alias:
			self.sort_by_translator(translator_alias=translator_alias)

		if self.sort_by_str and self.sort_by_str in self.all_sortings:
			self.all_chart_items = self.all_chart_items.order_by(self.sort_by_str)
			idx = self.all_sortings.index(self.sort_by_str)
			self.context[
				'date_of_translation_icon'] = ''  # Removing icon for default sort in order to prevent multiple icons
			self.context[self.all_sortings_context_links[idx][0]] = self.all_sortings_context_links[idx][1]
			self.context[self.all_sortings_context_links[idx][0] + '_icon'] = self.all_sortings_context_links[idx][2]
		else:
			self.all_chart_items = self.all_chart_items.order_by(self.base_sort_by)

	def sort_by(self, **kwargs):
		vn_with_instance = kwargs.get('vn_model').objects.filter(**kwargs.get('lookup')) \
			.select_related('genre') \
			.values_list('visual_novel_id')
		self.all_chart_items = self.all_chart_items.filter(visual_novel_id__in=vn_with_instance)
		try:
			instance = kwargs.get('model').objects.only('title', 'description').get(alias=kwargs.get('alias'))
			self.context['additional_breadcumb'] = self.chart_breadcumb_with_link + \
			                                       f"{kwargs.get('value')}: " + \
			                                       instance.title
			if instance.description:
				self.context['additional_description'] = instance.description
		except kwargs.get('model').DoesNotExist:
			pass

	def sort_by_staff(self, staff_alias: str):
		vn_with_staff = VNStaff.objects.filter(staff__alias=staff_alias).values('visual_novel')
		self.all_chart_items = self.all_chart_items.filter(visual_novel__in=vn_with_staff)
		try:
			staff = Staff.objects.only('title', 'description').get(alias=staff_alias)
			self.context['additional_breadcumb'] = self.chart_breadcumb_with_link + 'персона: ' + staff.title
			if staff.description:
				self.context['additional_description'] = staff.description
		except Staff.DoesNotExist:
			pass

	def sort_by_duration(self, duration_alias: str):
		self.all_chart_items = self.all_chart_items.filter(visual_novel__longevity__alias=duration_alias)
		try:
			duration = Longevity.objects.only('title', 'description').get(alias=duration_alias)
			self.context[
				'additional_breadcumb'] = self.chart_breadcumb_with_link + 'продолжительность: ' + duration.title
		except Longevity.DoesNotExist:
			pass

	def sort_by_translator(self, translator_alias: str):
		translators_ids = ChartItemTranslator.objects.filter(translator__alias=translator_alias) \
			.values_list('item__id', flat=True)
		self.all_chart_items = self.all_chart_items.filter(id__in=translators_ids)
		try:
			translator = Translator.objects.only('title', 'description', 'url').get(alias=translator_alias)
			self.context['additional_breadcumb'] = self.chart_breadcumb_with_link + 'переводчик: ' + translator.title
			if translator.description or translator.url:
				self.context['additional_description'] = ''
				translator_description = list()
				if translator.description:
					translator_description.append(translator.description)
				if translator.url:
					translator_description.append(f'<a href="{translator.url}">Ссылка на сайт переводчика.</a>')
				self.context['additional_description'] = '<br /><br />'.join(translator_description)
		except Translator.DoesNotExist:
			pass

	def serialize(self):
		genres_prefetch = Prefetch(
			'visual_novel__vngenre_set',
			queryset=VNGenre.objects.order_by('-weight').select_related('genre'),
		)
		studios_prefetch = Prefetch(
			'visual_novel__vnstudio_set',
			queryset=VNStudio.objects.order_by('-weight').select_related('studio'),
		)

		self.all_chart_items = self.all_chart_items.prefetch_related(genres_prefetch)
		self.all_chart_items = self.all_chart_items.prefetch_related(studios_prefetch)

		all_chart_items_data = ChartItemListSerializer(self.all_chart_items, many=True).data

		# Visual novels are grouped in list in groups of settings.CHART_NUMBER_OF_VN_IN_ROW
		k = 0
		row = list()

		for chart_item in all_chart_items_data:
			row.append(chart_item)
			k += 1
			if k % self.max_vn_by_row == 0:
				self.rows.append(row)
				row = list()

		if 0 < len(row) < settings.CHART_NUMBER_OF_VN_IN_ROW:
			self.rows.append(row)
