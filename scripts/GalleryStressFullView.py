#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import commands
import string
import time
import sys
import util

u = util.Util()

PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '/.app.Gallery'

class GalleryTest(unittest.TestCase):
    def setUp(self):
        super(GalleryTest,self).setUp()
        u._clearAllResource()
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()

    def tearDown(self):
        super(GalleryTest,self).tearDown()
        u.pressBack(4)

    def testCropPicture(self):
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Crop').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testCropPictureCancel(self):
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Cancel').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testAddEvent(self):
        u.setMenuOptions('Details')
        for i in range(100):
            d(resourceId = 'com.intel.android.gallery3d:id/event_edit').click.wait()
            d(text = 'Enter new event').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new event').set_text('NewEvent')
            self._tapOnDoneButton()
            assert d(text = 'NewEvent',resourceId = 'com.intel.android.gallery3d:id/event_text').wait.exists(timeout = 2000)
            #Delete the added event
            d(resourceId = 'com.intel.android.gallery3d:id/event_edit').click.wait()
            d(resourceId = 'com.intel.android.gallery3d:id/search_text_clear').click.wait() #Tap on X button to clear event
            self._tapOnDoneButton()
            assert d(text = 'Add an event').wait.exists(timeout = 2000)

    def testAddPlace(self):
        u.setMenuOptions('Details')
        for i in range(100):
            d(resourceId = 'com.intel.android.gallery3d:id/venue_edit').click.wait()
            d(text = 'Enter new venue').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new venue').set_text('NewVenue')
            self._tapOnDoneButton()
            assert d(text = 'NewVenue',resourceId = 'com.intel.android.gallery3d:id/venue_text').wait.exists(timeout = 2000)
            #Delete the added place
            d(resourceId = 'com.intel.android.gallery3d:id/venue_edit').click.wait()
            d(resourceId = 'com.intel.android.gallery3d:id/search_text_clear').click.wait() #Tap on X button to clear venue
            self._tapOnDoneButton()
            assert d(text = 'Add an venue').wait.exists(timeout = 2000)

    def testTagOnePicture(self):
        u.setMenuOptions('Details')
        for i in range(100):
            d.swipe(500,1050,500,200) #Swipe detail list up
            d(resourceId = 'com.intel.android.gallery3d:id/addKeywordButton').click.wait()
            d(text = 'Enter new keyword').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new keyword').set_text('NewKeyword')
            self._tapOnDoneButton()
            assert d(text = 'NewKeyword',className = 'android.widget.TextView').wait.exists(timeout = 2000)

    def testSetAsContact(self):
        for i in range(100):
            self._setPicAs('Contact')
            u.tapOnCenter() #Select the contact in the center of the list
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            d(text = 'Crop').click.wait()
            assert d(description = 'Share').wait.exists(timeout = 2000)

    def testSetAsWallpaper(self):
        for i in range(100):
            self._setPicAs('wallpaper')
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            d(text = 'Crop').click.wait()
            assert d(description = 'Share').wait.exists(timeout = 2000)

    def testViewPicture(self):
        for i in range(100):
            d.press('back') #If it goes to fullview suc, it shall back to the grid view after pressing back key
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')

    def testUPIcon(self):
        for i in range(100):
            d(resourceId = 'android:id/home').click.wait()
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')
            u.showPopCard()

    def testSlidePicture(self):
        for i in range(10):
            self._slideImageRtoL()
            for j in range(10):
                self._slideImageLtoR()

    def testDeleteOneByOne(self):
        self._clearAndPush500Pic()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            d(description = 'Delete').click.wait()
            d(text = 'Delete').click.wait() #Confirm it

    def testPlayPauseVideo(self):
        self._clearAndPushVideo()
        u.launchGallery()
        u.enterXView('fullview')
        for i in range(100):
            u.showPopCard()
            u.tapOnCenter() #Press playback icon
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            time.sleep(10) #Play video file 10 s
            u.showPopCard() #Invoke pop card
            u.tapOnCenter() #Pause the video playback
            assert d(resourceId = 'com.intel.android.gallery3d:id/background_play_action_provider_button').wait.exists(timeout = 2000)
            d(resourceId = 'android:id/home').click.wait() #Back to the fullview


















    def _clearAndPushVideo(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        commands.getoutput('adb push ' + sys.path[0] + 'resource/testvideo/ ' + '/sdcard/testvideo')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _clearAndPush500Pic(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        commands.getoutput('adb push ' + sys.path[0] + 'resource/Stress500pic/ /sdcard/Stress500pic')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _setPicAs(self,setact):
        d.press('menu')
        d(text = 'Set picture as').click.wait()
        setmode = {'contact':'Contact photo', 'wallpaper':'com.intel.android.gallery3d'}
        d(text = setmode[setact]).click.wait()

    def _tapOnDoneButton(self):
        #Touch on Done button on the soft keyboard
        d.click(650,1130)

    def _slideImageRtoL(self):
        #Swipe screen from right to left
        d.swipe(650,300,60,300,2)
        time.sleep(2)

    def _slideImageLtoR(self):
        #Swipe screen from left to right
        d.swipe(60,300,650,300,2)
        time.sleep(2)