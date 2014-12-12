'''
Contains notification services for android
    
Added
-New module

To Do
Currently the method showing creates a notification every 20 seconds while the app is open.  When closed nothing happens.
-A few options to explore to make this work
    -make the intent passed to alarm manager self.notification() (this would sidestep the need for a service and would be the cleanest implementation 
        -can pick up the intent with on_new_intent method
            http://python4dads.wordpress.com/2014/07/23/kivy-problems-with-on_new_intent-in-apps/
        -can explore how the python method was run here
            https://github.com/kivy/python-for-android/blob/3c669dccd159db1c87c4fd5f28f29acd79547e88/recipes/android/src/android/broadcast.py
    -make this a background service (less clean)
        -the python for android method for creating an AndroidService will only create a foreground service (with a permanent notificaiton)
        -Will need to create this service using pyjnius
        -this method would probably (maybe) be easier to implement
        
-when notification is touched take to three drops page of app
-when app is killed make touching notification restart app at three drops page

Future
-create the schedule at phone boot up (currently will only start after app is started)
       
'''

from datetime import datetime, timedelta, time  
from jnius import autoclass  
from android.broadcast import BroadcastReceiver


System = autoclass ('java.lang.System')
Context = autoclass('android.content.Context') 
IntentFilter = autoclass('android.content.IntentFilter')
Intent = autoclass('android.content.Intent')  
PendingIntent = autoclass('android.app.PendingIntent')  
Calendar = autoclass('java.util.Calendar') 
AlarmManager = autoclass('android.app.AlarmManager')  
AndroidString = autoclass('java.lang.String')  
NotificationBuilder = autoclass('android.app.Notification$Builder')

activity = autoclass('org.renpy.android.PythonActivity').mActivity
            
            
class Scheduler(object):  
    PENDING_INTENT_REQUEST_CODE = 889754
    #SCHEDULE_TIMES = [
    #    time(14, 10),              
    #]            
            
    #makes new schedule
    def create_alarm(self):
        #create broadcast receiver to receive intent from alarm manager
        br = BroadcastReceiver(self.notification, ['provider_changed'])
        br.context = activity
        br.start()
        #create schedule in alarm manager
        calendar = Calendar.getInstance()
        calendar.setTimeInMillis(System.currentTimeMillis());
        calendar.add(Calendar.SECOND, 60)
        alarm = activity.getSystemService(Context.ALARM_SERVICE)
        intent = Intent(Intent.ACTION_PROVIDER_CHANGED)
        pending_intent = PendingIntent.getBroadcast(activity, 0, intent, 0)
        alarm.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), 1000 * 20, pending_intent)
    
        
    #calculates the datetime of the defined SCHEDULE_TIMES
    def alarm_time(self):
        pass
        #today = datetime.now().date()
        #tomorrow = (datetime.now() + timedelta(days=1)).date()
        #candidates = [datetime.combine(today, schedule_time) for schedule_time in self.SCHEDULE_TIMES]
        #candidates += [datetime.combine(tomorrow, schedule_time) for schedule_time in self.SCHEDULE_TIMES]
        #candidates = [candidate for candidate in candidates if candidate > datetime.now()]
        #candidates.sort()
        #return candidates[0]
    
    
    def cancel_schedule(self):
        intent = Intent(Intent.ACTION_PROVIDER_CHANGED)
        pending_intent = PendingIntent.getBroadcast(activity, 0, intent, 0)
        alarm = activity.getSystemService(Context.ALARM_SERVICE)
        alarm.cancel(pending_intent)
        pending_intent.cancel()
    
    
    #builds notification
    def notification(self, *args):
        Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))

        notification_service = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        icon = getattr(Drawable, 'icon')   #takes the icon used as the app icon in the buildozer build

        notification_builder = NotificationBuilder(activity)

        title = AndroidString("Ocean Drops".encode('utf-8'))
        message = AndroidString("Write three good things".encode('utf-8'))

        java_class = autoclass('org.renpy.android.PythonActivity')().getClass()
        notificationIntent = Intent(activity, java_class)
        notificationIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP)

        intent = PendingIntent.getActivity(activity, 0, notificationIntent, 0)

        notification_builder.setContentTitle(title)
        notification_builder.setContentText(message)
        notification_builder.setContentIntent(intent)

        notification_builder.setSmallIcon(icon)
        notification_builder.setAutoCancel(True)
        notification_service.notify(0, notification_builder.build())