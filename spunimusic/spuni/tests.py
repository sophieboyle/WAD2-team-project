from django.test import TestCase
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from spuni.forms import LoginForm, UserForm, UserProfileForm, SongForm, EditUserProfileForm
from spuni.views import upvote, downvote, filter_out_zero_votes

"""
    Tests the index view.
"""
class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_location_spuni(self):
        """
            Tests that the location of the view
            corresponds to the expected hardcoded url.
        """
        response = self.client.get('/spuni/')
        self.assertEqual(response.status_code, 200)
    
    def test_location_blank(self):
        """
            Tests that the index view can be invoked
            by a blank hardcoded url. 
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
    def test_url_accessibility(self):
        """
           Tests that the index view can be invoked
           by the expected relative view. 
        """
        response = self.client.get(reverse('spuni:index'))
        self.assertEquals(response.status_code, 200)
    
    def test_correct_template(self):
        """
            Tests that the index view uses its
            corresponding template.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

"""
    Test the helper function filter_out_zero_votes.
"""
class filterOutZeroVoteSongsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
            upvotes=100)
        Song.objects.create(name="Redbone", artist="Childish Gambino",
                    albumArt='https://i.scdn.co/image/ab67616d0000b273b08b996d08001270adc8b555',
                    upvotes=0)
    
    def test_no_zeros(self):
        """
            Tests that no songs with zero upvotes are
            included in the return list, and only songs
            which have upvotes > 0 remain in the result.
        """
        song_list = Song.objects.order_by('-upvotes')
        result = filter_out_zero_votes(song_list)
        self.assertFalse(Song.objects.get(slug="redbone-childish-gambino") in result)
        self.assertTrue(Song.objects.get(slug="shiba-inus-are-the-best-shibe1") in result)
"""
    Tests the show_song view.
"""
class ShowSongViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                    albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                    upvotes=10)
    
    def test_slug_param(self):
        """
            Tests that the song view works when passing the
            song slug as a parameter to the view.
        """
        slug = "shiba-inus-are-the-best-shibe1"
        song = Song.objects.get(slug=slug)
        response = self.client.get(reverse('spuni:show_song', args=(slug,)))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        """
            Tests that the correct corresponding
            template is used for the show_song view.
        """
        slug = "shiba-inus-are-the-best-shibe1"
        song = Song.objects.get(slug=slug)
        response = self.client.get(reverse('spuni:show_song', args=(slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'song.html')
    
    def test_location(self):
        """
            Tests that the view can be invoked by the
            expected hardcoded url.
        """
        slug = "shiba-inus-are-the-best-shibe1"
        response = self.client.get('/spuni/song/'+slug+'/')
        self.assertEqual(response.status_code, 200)

"""
    Tests the show_profile view.
"""
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
        """
            Tests that the profile view can be invoked by
            passing the username to the relative view.
        """
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get(reverse('spuni:show_profile', args=("testshibe",)))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        """
            Tests that the corresponding template
            is used for the show_profile view.
        """
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get(reverse('spuni:show_profile', args=("testshibe",)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
    
    def test_location(self):
        """
            Tests that the show_profile view can be
            invoked by the expected hardcoded url.
        """
        login = self.client.login(username="authshibe", password="iamauthshibe")
        response = self.client.get('/spuni/profile/testshibe/')
        self.assertEqual(response.status_code, 200)

"""
    Tests the search view.
"""
class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Redbone", artist="Childish Gambino",
                            albumArt='https://i.scdn.co/image/ab67616d0000b273b08b996d08001270adc8b555',
                            upvotes=55)

    def test_location(self):
        """
            Tests that the search view can be invoked
            by the expected hardcoded url.
        """
        response = self.client.get('/spuni/search/redbone/')
        self.assertEqual(response.status_code, 200)

    def test_query_with_spaces(self):
        """
            Test that the search view works correctly
            with a query with spaces and capital letters.
        """
        response = self.client.get(reverse("spuni:search_song", args=("Platinum Disco",)))
        self.assertEqual(response.status_code, 200)
    
    def test_get_by_name(self):
        """
            Test that the search view can be invoked
            by the expected relative url with a query argument.
        """
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        """
            Test that the corresponding template for 
            the search view is being used.
        """
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
    
    def test_context_songs_have_upvote_field(self):
        """
            Test that the search view correctly populates context_dict
            song records with an upvote field.
        """
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        self.assertTrue("upvotes" in response.context['songs'][0])
    
    def test_context_has_existing_models(self):
        """
            Test that the search view correctly populates context_dict
            song records for song instances which already exist, with
            their expected number of upvotes.
        """
        response = self.client.get(reverse("spuni:search_song", args=("redbone",)))
        for song_id in response.context['songs'].keys():
            if (response.context['songs'][song_id]["name"] == "Redbone") and (response.context['songs'][song_id]["artist_name"] == "Childish Gambino"):
                result = song_id
                break
        self.assertEquals(response.context['songs'][song_id]['upvotes'], 55)

    def test_new_slugs_for_spotify_entries(self):
        """
            Test that the search view correctly populates context_dict
            with slugs consisting of both the song name and artist.
        """
        response = self.client.get(reverse("spuni:search_song", args=("Platinum Disco",)))
        expected_slug = slugify(response.context["songs"][0]["name"])+'-'+slugify(response.context["songs"][0]["artist_name"])
        self.assertTrue(response.context["songs"][0]["slug"] == expected_slug)

"""
    Tests the user_login view.
"""
class UserLoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_login_view_post(self):
        """
            Tests that the user is logged in correctly and
            is redirected to the index page.
        """
        credentials = {"username" : "testshibe",
                        "password" : "iamtestshibe"}
        response = self.client.post("/spuni/login/", credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)
        self.assertRedirects(response, reverse("spuni:index"))        

    def test_login_view_get(self):
        """
            Tests that a login form is presented
            upon a get request.
        """
        response = self.client.get(reverse("spuni:login"))
        self.assertEquals(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'], LoginForm))

    def test_invalid_login(self):
        """
            Test that an invalid login returns a httpresponse
            describing the error.
        """
        invalid_creds = {"username" : "testshibe",
                        "password" : "iambadshibe"}
        response = self.client.post("/spuni/login/", invalid_creds, follow=True)
        self.assertEqual(response.content, b"Invalid login details.")

    def test_location(self):
        """
            Test that the login view can be accessed
            by the expected hardcoded path.
        """
        response = self.client.get("/spuni/login/")
        self.assertEquals(response.status_code, 200)
    
    def test_uses_correct_template(self):
        """
            Test that the login form uses the 
            corresponding template.
        """
        response = self.client.get(reverse("spuni:login"))
        self.assertTemplateUsed("login.html")

"""
    Tests the register view.
"""
class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_register_view_get(self):
        """
            Test that the register view presents
            a register form upon a get request.
        """
        response = self.client.get(reverse("spuni:register"))
        self.assertEquals(response.status_code, 200)
        self.failUnless(isinstance(response.context["form"], UserForm))

    def test_register_view_post(self):
        """
            Test that the register view registers a user
            with the correct details upon a post request.
        """
        details = {"username" : "signupshibe",
                    "password" : "iamsignupshibe",
                    "email" : "signupshibe@shibemail.com",
                    "photo" : "https://66.media.tumblr.com/207afd29ee5a60a30985389c63a5b51d/tumblr_pgo9ulfB2o1valbo1_400.jpg"}
        response = self.client.post(reverse("spuni:register"), data=details)
        self.assertTrue(User.objects.filter(username="signupshibe").exists())
        self.assertTrue(UserProfile.objects.filter(user=User.objects.get(username="signupshibe")).exists())
        self.assertTrue(response.context["registered"])

    def test_invalid_registration_user_already_exists(self):
        """
            Test that a user is not registered upon
            a post request if the details are invalid.
        """
        details = {"username" : "testshibe",
                    "password" : "iamtestshibe",
                    "email" : "testshibe@shibemail.com",
                    "photo" : "https://66.media.tumblr.com/207afd29ee5a60a30985389c63a5b51d/tumblr_pgo9ulfB2o1valbo1_400.jpg"}
        response = self.client.post(reverse("spuni:register"), data=details)
        self.assertFalse(response.context["registered"])

    def test_location(self):
        """
            Test that the register view can be invoked
            by the expected hardcoded path.
        """
        response = self.client.get("/spuni/register/")
        self.assertEquals(response.status_code, 200)
    
    def test_uses_correct_template(self):
        """
            Test that the register view uses
            the corresponding template.
        """
        response = self.client.get(reverse("spuni:register"))
        self.assertTemplateUsed("register.html")

"""
    Tests the edit_profile view.
"""
class EditProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_edit_post(self):
        """
            Test that the user's profile image url is
            updated upon a post request when logged in.
        """
        new_img = "https://66.media.tumblr.com/a64d88296ba34d1bec4fd8e833d711ea/tumblr_ohtx6cUWOi1voqnhpo3_250.png"
        self.client.login(username="testshibe", password="iamtestshibe")
        response = self.client.post(reverse("spuni:edit_profile"), {"photo" : new_img})
        test_user = user=User.objects.get(username="testshibe")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.get(user=test_user).photo, new_img)
        self.assertTrue(response.context["edited"])

    def test_edit_get(self):
        """
            Test that the edit_profile view provides
            a form to edit upon a get request.
        """
        self.client.login(username="testshibe", password="iamtestshibe")
        response = self.client.get(reverse("spuni:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["edited"])
        self.failUnless(isinstance(response.context["edit_form"], EditUserProfileForm))

    def test_location(self):
        """
            Test that the edit_profile view can
            be accessed via the expected hardcoded url.
        """
        self.client.login(username="testshibe", password="iamtestshibe")
        response = self.client.get("/spuni/edit/")
        self.assertEqual(response.status_code, 200)
    
    def test_uses_correct_template(self):
        """
            Test that the edit_profile view uses
            the correct template.
        """
        self.client.login(username="testshibe", password="iamtestshibe")
        response = self.client.get(reverse("spuni:edit_profile"))
        self.assertTemplateUsed("edit.html")

"""
    Tests the upvote helper function.
"""
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
        """
            Tests that a song is upvoted when the
            slug is passed as a parameter.
        """
        test_slug = "shiba-inus-are-the-best-shibe1"
        upvote({"username":"testshibe", "slug":test_slug})
        self.assertTrue(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertEquals(Song.objects.get(slug="shiba-inus-are-the-best-shibe1").upvotes, self.pre_upvote_count + 1)

    def test_add_upvote_to_new_song_with_dict_all_details(self):
        """
            Test that a new song is created and upvoted if
            the instance does not already exist, and if all
            details are provided.
        """
        song_details = {"username" : "testshibe",
                        "slug" : "careless-whisper-george-michael",
                        "name" : "Careless Whisper",
                        "albumArt" : "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Wham%21_featuring_George_Michael_US_release.jpeg/220px-Wham%21_featuring_George_Michael_US_release.jpeg",
                        "artist" : "George Michael"}
        upvote(song_details)
        self.assertTrue(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=song_details["slug"]).exists())
        self.assertEqual(Song.objects.get(slug=song_details["slug"]).upvotes, 1)

"""
    Tests the downvote helper function.
"""
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
        """
            Test that a song is downvote when provided
            a slug.
        """
        test_slug = "shiba-inus-are-the-best-shibe1"
        downvote({"username" : "testshibe", "slug" : "shiba-inus-are-the-best-shibe1"})
        self.assertFalse(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertEqual(Song.objects.get(slug=test_slug).upvotes, self.pre_downvote_count)

    def test_downvote_on_non_existing_song(self):
        """
            Test that a song is not downvoted if it
            is not yet an instance (i.e. it has never
            been upvoted before.)
        """
        test_slug = "careless-whisper-george-michael"
        downvote({"username" : "testshibe", "slug" : test_slug})
        self.assertFalse(UserProfile.objects.get(user=self.test_user).upvotedSongs.filter(slug=test_slug).exists())
        self.assertFalse(Song.objects.filter(slug=test_slug).exists())

"""
    Tests the Song model.
"""
class SongModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                            upvotes=10)

    def test_slug_construction(self):
        """
            Test that the song slug is constructed
            with the name and artist slugs correctly.
        """
        song = Song.objects.get(id=1)
        name = song.name
        artist = song.artist
        slug = song.slug
        self.assertEquals(slug, f"{slugify(name)}-{slugify(artist)}")

    def test_name_label(self):
        """
            Test that the name label is correct.
        """
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")
    
    def test_album_art_label(self):
        """
            Test that the albumArt label is correct.
        """
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("albumArt").verbose_name
        self.assertEquals(field_label, "albumArt")
    
    def test_upvotes_label(self):
        """
            Test that the upvotes label is correct.
        """
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("upvotes").verbose_name
        self.assertEquals(field_label, "upvotes")
    
    def test_artist_label(self):
        """
            Test that the artist label is correct.
        """
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("artist").verbose_name
        self.assertEquals(field_label, "artist")
    
    def test_slug_label(self):
        """
            Test that the slug label is correct.
        """
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")
    
    def test_name_max_length(self):
        """
            Test that the max length of the name
            field is as expected.
        """
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("name").max_length
        self.assertEquals(max_length, 128)
    
    def test_artist_max_length(self):
        """
            Test that the max length of the artist
            field is as expected.
        """
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("artist").max_length
        self.assertEquals(max_length, 128)
    
    def test_album_art_max_length(self):
        """
            Test that the max length of the albumArt
            field is as expected.
        """
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("albumArt").max_length
        self.assertEquals(max_length, 200)
    
    def test_str(self):
        """
            Tests that the str method returns
            the song's name as expected.
        """
        song = Song.objects.get(id=1)
        self.assertEquals(str(song), song.name)

"""
    Tests the UserProfile model.
"""
class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_user_label(self):
        """
            Test user label is correct.
        """
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("user").verbose_name
        self.assertEquals(user_label, "user")
    
    def test_photo_label(self):
        """
            Test photo label is correct.
        """
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("photo").verbose_name
        self.assertEquals(user_label, "photo")

    def test_upvoted_songs_label(self):
        """
            Test upvotedSongs label is correct.
        """
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("upvotedSongs").verbose_name
        self.assertEquals(user_label, "upvotedSongs")
    
    def test_photo_max_length(self):
        """
            Test that the max length of the photo
            field is as expected.
        """
        up = UserProfile.objects.get(id=1)
        max_length = up._meta.get_field("photo").max_length
        self.assertEquals(max_length, 200)