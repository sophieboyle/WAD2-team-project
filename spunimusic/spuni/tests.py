from django.test import TestCase
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_location_spuni(self):
        response = self.client.get('/spuni/')
        self.assertEqual(response.status_code, 200)
    
    def test_location_blank(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
    def test_url_accessibility(self):
        response = self.client.get(reverse('spuni:index'))
        self.assertEquals(response.status_code, 200)
    
    def test_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class ShowSongViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                    albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                    upvotes=10)
    
    def test_slug_param(self):
        slug = "shiba-inus-are-the-best-shibe1"
        song = Song.objects.get(slug=slug)
        response = self.client.get(reverse('spuni:show_song', args=(slug,)))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        slug = "shiba-inus-are-the-best-shibe1"
        song = Song.objects.get(slug=slug)
        response = self.client.get(reverse('spuni:show_song', args=(slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'song.html')
    
    def test_location(self):
        slug = "shiba-inus-are-the-best-shibe1"
        response = self.client.get('/spuni/song/'+slug+'/')
        self.assertEqual(response.status_code, 200)

class ShowProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

        u2 = User.objects.create_user(username="authshibe")
        u2.set_password("iamauthshibe")
        u2.save()
        UserProfile.objects.create(user=u2,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_username_param(self):
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get(reverse('spuni:show_profile', args=("testshibe",)))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get(reverse('spuni:show_profile', args=("testshibe",)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
    
    def test_location(self):
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get('/spuni/profile/testshibe/')
        self.assertEqual(response.status_code, 200)
    
class SearchViewTest(TestCase):
    def test_location(self):
        response = self.client.get('/spuni/search/redbone/')
        self.assertEqual(response.status_code, 200)

    def test_query_with_spaces(self):
        response = self.client.get(reverse("spuni:search_song", args=("Platinum Disco",)))
        self.assertEqual(response.status_code, 200)
    
    def test_get_by_name(self):
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")

class UserLoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_login(self):
        credentials = {"username" : "testshibe",
                        "password" : "iamtestshibe"}
        response = self.client.post("/spuni/login/", credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)        

class SongModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                            upvotes=10)
    
    def test_slug_construction(self):
        song = Song.objects.get(id=1)
        name = song.name
        artist = song.artist
        slug = song.slug
        self.assertEquals(slug, f"{slugify(name)}-{slugify(artist)}")

    def test_name_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")
    
    def test_album_art_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("albumArt").verbose_name
        self.assertEquals(field_label, "albumArt")
    
    def test_upvotes_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("upvotes").verbose_name
        self.assertEquals(field_label, "upvotes")
    
    def test_artist_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("artist").verbose_name
        self.assertEquals(field_label, "artist")
    
    def test_slug_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")
    
    def test_name_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("name").max_length
        self.assertEquals(max_length, 128)
    
    def test_artist_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("artist").max_length
        self.assertEquals(max_length, 128)
    
    def test_album_art_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("albumArt").max_length
        self.assertEquals(max_length, 200)
    
    def test_str(self):
        song = Song.objects.get(id=1)
        self.assertEquals(str(song), song.name)

class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_user_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("user").verbose_name
        self.assertEquals(user_label, "user")
    
    def test_photo_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("photo").verbose_name
        self.assertEquals(user_label, "photo")

    def test_upvoted_songs_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("upvotedSongs").verbose_name
        self.assertEquals(user_label, "upvotedSongs")
    
    def test_photo_max_length(self):
        up = UserProfile.objects.get(id=1)
        max_length = up._meta.get_field("photo").max_length
        self.assertEquals(max_length, 200)