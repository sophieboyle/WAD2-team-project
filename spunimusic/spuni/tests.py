from django.test import TestCase
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from spuni.forms import LoginForm, UserForm, UserProfileForm, SongForm
from spuni.views import upvote, downvote

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
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Redbone", artist="Childish Gambino",
                            albumArt='https://i.scdn.co/image/ab67616d0000b273b08b996d08001270adc8b555',
                            upvotes=55)

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
    
    def test_context_songs_have_upvote_field(self):
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertTrue("upvotes" in response.context['songs'][0])
    
    def test_context_has_existing_models(self):
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        for song_id in response.context['songs'].keys():
            if (response.context['songs'][song_id]["name"] == "Redbone") and (response.context['songs'][song_id]["artist_name"] == "Childish Gambino"):
                result = song_id
                break
        self.assertEquals(response.context['songs'][song_id]['upvotes'], 55)

    def test_new_slugs_for_spotify_entries(self):
        response = self.client.get(reverse("spuni:search_song", args=("Platinum Disco",)))
        expected_slug = slugify(response.context["songs"][0]["name"])+'-'+slugify(response.context["songs"][0]["artist_name"])
        self.assertTrue(response.context["songs"][0]["slug"] == expected_slug)

class UserLoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_login_view_post(self):
        credentials = {"username" : "testshibe",
                        "password" : "iamtestshibe"}
        response = self.client.post("/spuni/login/", credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)
        self.assertRedirects(response, reverse("spuni:index"))        

    def test_login_view_get(self):
        response = self.client.get(reverse("spuni:login"))
        self.assertEquals(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'], LoginForm))

    def test_invalid_login(self):
        invalid_creds = {"username" : "testshibe",
                        "password" : "iambadshibe"}
        response = self.client.post("/spuni/login/", invalid_creds, follow=True)
        self.assertEqual(response.content, b"Invalid login details.")

    def test_location(self):
        response = self.client.get("/spuni/login/")
        self.assertEquals(response.status_code, 200)
    
    def test_uses_correct_template(self):
        response = self.client.get(reverse("spuni:login"))
        self.assertTemplateUsed("login.html")

class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_register_view_get(self):
        response = self.client.get(reverse("spuni:register"))
        self.assertEquals(response.status_code, 200)
        self.failUnless(isinstance(response.context["form"], UserForm))

    def test_register_view_post(self):
        details = {"username" : "signupshibe",
                    "password" : "iamsignupshibe",
                    "email" : "signupshibe@shibemail.com",
                    "photo" : "https://66.media.tumblr.com/207afd29ee5a60a30985389c63a5b51d/tumblr_pgo9ulfB2o1valbo1_400.jpg"}
        response = self.client.post(reverse("spuni:register"), data=details)
        self.assertTrue(User.objects.filter(username="signupshibe").exists())
        self.assertTrue(UserProfile.objects.filter(user=User.objects.get(username="signupshibe")).exists())
        self.assertTrue(response.context["registered"])

    def test_invalid_registration_user_already_exists(self):
        details = {"username" : "testshibe",
                    "password" : "iamtestshibe",
                    "email" : "testshibe@shibemail.com",
                    "photo" : "https://66.media.tumblr.com/207afd29ee5a60a30985389c63a5b51d/tumblr_pgo9ulfB2o1valbo1_400.jpg"}
        response = self.client.post(reverse("spuni:register"), data=details)
        self.assertFalse(response.context["registered"])

    def test_location(self):
        response = self.client.get("/spuni/register/")
        self.assertEquals(response.status_code, 200)

class UpvoteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                            upvotes=10)
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def setUp(self):
        self.test_user =  User.objects.get(username="testshibe")
        self.test_song = Song.objects.get(slug="shiba-inus-are-the-best-shibe1")
        self.pre_upvote_count = self.test_song.upvotes

    def test_add_upvote_to_existing_song_with_dict_slug_only(self):
        test_slug = "shiba-inus-are-the-best-shibe1"
        upvote({"username":"testshibe", "slug":test_slug})
        self.assertTrue(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertEquals(Song.objects.get(slug="shiba-inus-are-the-best-shibe1").upvotes, self.pre_upvote_count + 1)

    def test_add_upvote_to_new_song_with_dict_all_details(self):
        song_details = {"username" : "testshibe",
                        "slug" : "careless-whisper-george-michael",
                        "name" : "Careless Whisper",
                        "albumArt" : "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Wham%21_featuring_George_Michael_US_release.jpeg/220px-Wham%21_featuring_George_Michael_US_release.jpeg",
                        "artist" : "George Michael"}
        upvote(song_details)
        self.assertTrue(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=song_details["slug"]).exists())
        self.assertEqual(Song.objects.get(slug=song_details["slug"]).upvotes, 1)

class DownvoteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                            upvotes=10)
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def setUp(self):
        self.test_user =  User.objects.get(username="testshibe")
        self.test_song = Song.objects.get(slug="shiba-inus-are-the-best-shibe1")
        self.pre_downvote_count = self.test_song.upvotes

    def test_downvote_on_existing_song(self):
        test_slug = "shiba-inus-are-the-best-shibe1"
        downvote({"username" : "testshibe", "slug" : "shiba-inus-are-the-best-shibe1"})
        self.assertFalse(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertEqual(Song.objects.get(slug=test_slug).upvotes, self.pre_downvote_count)

    def test_downvote_on_non_existing_song(self):
        test_slug = "careless-whisper-george-michael"
        downvote({"username" : "testshibe", "slug" : test_slug})
        self.assertFalse(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertFalse(Song.objects.filter(slug=test_slug).exists())

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