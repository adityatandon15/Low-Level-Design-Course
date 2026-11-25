import math
import time
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


# -------------------- Observer Pattern -------------------- #

# Observer Pattern: Interface for notification observers
class NotificationObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass


# Concrete observer
class UserNotificationObserver(NotificationObserver):
    def __init__(self, id):
        self.userId = id

    def update(self, message):
        print("Notification for user " + self.userId + ": " + message)


# Observable for Observer Pattern
class NotificationService:
    # Singleton Pattern
    _instance = None

    def __init__(self):
        self.observers = {}

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def registerObserver(self, userId, observer):
        self.observers[userId] = observer

    def removeObserver(self, userId):
        self.observers.pop(userId, None)

    def notifyUser(self, userId, message):
        if userId in self.observers:
            self.observers[userId].update(message)

    def notifyAll(self, message):
        for pair in list(self.observers.items()):
            pair[1].update(message)


# -------------------- Basic Models -------------------- #

# Gender enum
class Gender(Enum):
    MALE = 1
    FEMALE = 2
    NON_BINARY = 3
    OTHER = 4


# Location class
class Location:
    def __init__(self, lat=0.0, lon=0.0):
        self.latitude = lat
        self.longitude = lon

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def setLatitude(self, lat):
        self.latitude = lat

    def setLongitude(self, lon):
        self.longitude = lon

    # Calculate distance in kilometers between two locations using Haversine formula
    def distanceInKm(self, other):
        earthRadiusKm = 6371.0
        dLat = (other.latitude - self.latitude) * math.pi / 180.0
        dLon = (other.longitude - self.longitude) * math.pi / 180.0

        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
             math.cos(self.latitude * math.pi / 180.0) * math.cos(other.latitude * math.pi / 180.0) *
             math.sin(dLon / 2) * math.sin(dLon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earthRadiusKm * c


# Interest class
class Interest:
    def __init__(self, n="", c=""):
        self.name = n
        self.category = c

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category


# Preference class
class Preference:
    def __init__(self):
        self.interestedIn = []
        self.interests = []
        self.minAge = 18
        self.maxAge = 100
        self.maxDistance = 100.0  # in kilometers

    def addGenderPreference(self, gender):
        self.interestedIn.append(gender)

    def removeGenderPreference(self, gender):
        if gender in self.interestedIn:
            self.interestedIn.remove(gender)

    def setAgeRange(self, minAge, maxAge):
        self.minAge = minAge
        self.maxAge = maxAge

    def setMaxDistance(self, distance):
        self.maxDistance = distance

    def addInterest(self, interest):
        self.interests.append(interest)

    def removeInterest(self, interest):
        if interest in self.interests:
            self.interests.remove(interest)

    def isInterestedInGender(self, gender):
        return gender in self.interestedIn

    def isAgeInRange(self, age):
        return age >= self.minAge and age <= self.maxAge

    def isDistanceAcceptable(self, distance):
        return distance <= self.maxDistance

    def getInterests(self):
        return self.interests

    def getInterestedGenders(self):
        return self.interestedIn

    def getMinAge(self):
        return self.minAge

    def getMaxAge(self):
        return self.maxAge

    def getMaxDistance(self):
        return self.maxDistance


# -------------------- Message System -------------------- #

# Message class
class Message:
    def __init__(self, sender, msg):
        self.senderId = sender
        self.content = msg
        self.timestamp = int(time.time() * 1000)

    def getSenderId(self):
        return self.senderId

    def getContent(self):
        return self.content

    def getTimestamp(self):
        return self.timestamp

    def getFormattedTime(self):
        # SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        return datetime.fromtimestamp(self.timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")


# Chat room class
class ChatRoom:
    def __init__(self, roomId, user1Id, user2Id):
        self.id = roomId
        self.participantIds = []
        self.participantIds.append(user1Id)
        self.participantIds.append(user2Id)
        self.messages = []

    def getId(self):
        return self.id

    def addMessage(self, senderId, content):
        msg = Message(senderId, content)
        self.messages.append(msg)

    def hasParticipant(self, userId):
        return userId in self.participantIds

    def getMessages(self):
        return self.messages

    def getParticipants(self):
        return self.participantIds

    def displayChat(self):
        print("===== Chat Room: " + self.id + " =====")
        for msg in self.messages:
            print("[" + msg.getFormattedTime() + "] " + msg.getSenderId() + ": " + msg.getContent())
        print("=========================")


# -------------------- Profile System -------------------- #

# Profile class
class UserProfile:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.gender = Gender.OTHER
        self.bio = None
        self.photos = []
        self.interests = []
        self.location = Location()

    def setName(self, n):
        self.name = n

    def setAge(self, a):
        self.age = a

    def setGender(self, g):
        self.gender = g

    def setBio(self, b):
        self.bio = b

    def addPhoto(self, photoUrl):
        self.photos.append(photoUrl)

    def removePhoto(self, photoUrl):
        if photoUrl in self.photos:
            self.photos.remove(photoUrl)

    def addInterest(self, name, category):
        interest = Interest(name, category)
        self.interests.append(interest)

    def removeInterest(self, name):
        self.interests = [i for i in self.interests if i.getName() != name]

    def setLocation(self, loc):
        self.location = loc

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getGender(self):
        return self.gender

    def getBio(self):
        return self.bio

    def getPhotos(self):
        return self.photos

    def getInterests(self):
        return self.interests

    def getLocation(self):
        return self.location

    def display(self):
        print("===== Profile =====")
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Gender: ", end="")
        if self.gender == Gender.MALE:
            print("Male", end="")
        elif self.gender == Gender.FEMALE:
            print("Female", end="")
        elif self.gender == Gender.NON_BINARY:
            print("Non-binary", end="")
        elif self.gender == Gender.OTHER:
            print("Other", end="")
        print()
        bioText = "null" if self.bio is None else self.bio
        print("Bio: " + bioText)
        print("Photos: ", end="")
        for photo in self.photos:
            print(photo + ", ", end="")
        print()
        print("Interests: ", end="")
        for i in self.interests:
            print(i.getName() + " (" + i.getCategory() + "), ", end="")
        print()
        print("Location: " + str(self.location.getLatitude()) + ", " + str(self.location.getLongitude()))
        print("===================")


# -------------------- User System -------------------- #

# Swipe action enum
class SwipeAction(Enum):
    LEFT = 1   # Dislike
    RIGHT = 2  # Like


# User class
class User:
    def __init__(self, userId):
        self.id = userId
        self.profile = UserProfile()
        self.preference = Preference()
        self.swipeHistory = {}    # userId -> action
        self.notificationObserver = UserNotificationObserver(userId)
        NotificationService.getInstance().registerObserver(userId, self.notificationObserver)

    def getId(self):
        return self.id

    def getProfile(self):
        return self.profile

    def getPreference(self):
        return self.preference

    def swipe(self, otherUserId, action):
        self.swipeHistory[otherUserId] = action

    def hasLiked(self, otherUserId):
        return otherUserId in self.swipeHistory and self.swipeHistory[otherUserId] == SwipeAction.RIGHT

    def hasDisliked(self, otherUserId):
        return otherUserId in self.swipeHistory and self.swipeHistory[otherUserId] == SwipeAction.LEFT

    def hasInteractedWith(self, otherUserId):
        return otherUserId in self.swipeHistory

    def displayProfile(self):  # Principle of least knowledge
        self.profile.display()


# -------------------- Location Service -------------------- #

# Strategy Pattern: Location service strategy interface
class LocationStrategy(ABC):
    @abstractmethod
    def findNearbyUsers(self, location, maxDistance, allUsers):
        pass


# Concrete strategy: Basic location strategy
class BasicLocationStrategy(LocationStrategy):
    def findNearbyUsers(self, location, maxDistance, allUsers):
        nearbyUsers = []
        for user in allUsers:
            distance = location.distanceInKm(user.getProfile().getLocation())
            if distance <= maxDistance:
                nearbyUsers.append(user)
        return nearbyUsers


# Location service with Strategy Pattern
class LocationService:
    # Singleton Pattern
    _instance = None

    def __init__(self):
        self.strategy = BasicLocationStrategy()

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def setStrategy(self, newStrategy):
        self.strategy = newStrategy

    def findNearbyUsers(self, location, maxDistance, allUsers):
        return self.strategy.findNearbyUsers(location, maxDistance, allUsers)


# -------------------- Matching System -------------------- #

class MatcherType(Enum):
    BASIC = 1
    INTERESTS_BASED = 2
    LOCATION_BASED = 3


# Matcher interface
class Matcher(ABC):
    @abstractmethod
    def calculateMatchScore(self, user1, user2):
        pass


# Concrete matcher: Basic matcher
class BasicMatcher(Matcher):
    def calculateMatchScore(self, user1, user2):
        # Basic scoring, just check if preferences align
        user1LikesUser2Gender = user1.getPreference().isInterestedInGender(user2.getProfile().getGender())
        user2LikesUser1Gender = user2.getPreference().isInterestedInGender(user1.getProfile().getGender())

        if not user1LikesUser2Gender or not user2LikesUser1Gender:
            return 0.0

        # Check age preference
        user1LikesUser2Age = user1.getPreference().isAgeInRange(user2.getProfile().getAge())
        user2LikesUser1Age = user2.getPreference().isAgeInRange(user1.getProfile().getAge())

        if not user1LikesUser2Age or not user2LikesUser1Age:
            return 0.0

        # Check distance preference
        distance = user1.getProfile().getLocation().distanceInKm(user2.getProfile().getLocation())
        user1LikesUser2Distance = user1.getPreference().isDistanceAcceptable(distance)
        user2LikesUser1Distance = user2.getPreference().isDistanceAcceptable(distance)

        if not user1LikesUser2Distance or not user2LikesUser1Distance:
            return 0.0

        # If all basic criteria match, return a base score
        return 0.5  # 50% match


# Concrete matcher: Interests-based matcher
class InterestsBasedMatcher(Matcher):
    def calculateMatchScore(self, user1, user2):
        # First, check basic compatibility
        basicMatcher = BasicMatcher()
        baseScore = basicMatcher.calculateMatchScore(user1, user2)

        if baseScore == 0.0:
            return 0.0  # No need to continue if basic criteria don't match

        # Calculate score based on shared interests
        user1InterestNames = []
        for interest in user1.getProfile().getInterests():
            user1InterestNames.append(interest.getName())

        sharedInterests = 0
        for interest in user2.getProfile().getInterests():
            if interest.getName() in user1InterestNames:
                sharedInterests += 1

        # Bonus score based on shared interests (up to 0.5 additional points)
        maxInterests = max(len(user1.getProfile().getInterests()), len(user2.getProfile().getInterests()))
        interestScore = 0.5 * (float(sharedInterests) / maxInterests) if maxInterests > 0 else 0.0

        return baseScore + interestScore


# Concrete matcher: Location-based matcher
class LocationBasedMatcher(Matcher):
    def calculateMatchScore(self, user1, user2):
        # First, check basic compatibility
        interestsMatcher = InterestsBasedMatcher()
        baseScore = interestsMatcher.calculateMatchScore(user1, user2)

        if baseScore == 0.0:
            return 0.0  # No need to continue if basic criteria don't match

        # Calculate score based on proximity
        distance = user1.getProfile().getLocation().distanceInKm(user2.getProfile().getLocation())
        maxDistance = min(user1.getPreference().getMaxDistance(), user2.getPreference().getMaxDistance())

        # Closer is better, score decreases with distance (up to 0.2 additional points)
        proximityScore = 0.2 * (1.0 - (distance / maxDistance)) if maxDistance > 0 else 0.0

        return baseScore + proximityScore


# Factory Pattern: Matcher factory
class MatcherFactory:
    @staticmethod
    def createMatcher(type):
        if type == MatcherType.BASIC:
            return BasicMatcher()
        elif type == MatcherType.INTERESTS_BASED:
            return InterestsBasedMatcher()
        elif type == MatcherType.LOCATION_BASED:
            return LocationBasedMatcher()
        else:
            return BasicMatcher()


# -------------------- Dating App -------------------- #

# Facade Pattern: Dating app system
class DatingApp:
    # Singleton Pattern
    _instance = None

    def __init__(self):
        self.users = []
        self.chatRooms = []

        # Default to location-based matcher
        self.matcher = MatcherFactory.createMatcher(MatcherType.LOCATION_BASED)

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def setMatcher(self, type):
        self.matcher = MatcherFactory.createMatcher(type)

    def createUser(self, userId):
        user = User(userId)
        self.users.append(user)
        return user

    def getUserById(self, userId):
        for user in self.users:
            if user.getId() == userId:
                return user
        return None

    def findNearbyUsers(self, userId, maxDistance):
        user = self.getUserById(userId)
        if user is None:
            return []

        # Find users within maxDistance km
        nearbyUsers = LocationService.getInstance().findNearbyUsers(
            user.getProfile().getLocation(), maxDistance, self.users)

        # Filter out the user themselves
        if user in nearbyUsers:
            nearbyUsers.remove(user)

        # Filter out users that don't match preferences or have already been swiped
        filteredUsers = []
        for otherUser in nearbyUsers:
            # Skip users that have already been interacted with
            if not user.hasInteractedWith(otherUser.getId()):

                # Calculate match score
                score = self.matcher.calculateMatchScore(user, otherUser)

                # If score is above 0, they meet basic preference criteria
                if score > 0:
                    filteredUsers.append(otherUser)

        return filteredUsers

    def swipe(self, userId, targetUserId, action):
        user = self.getUserById(userId)
        targetUser = self.getUserById(targetUserId)

        if user is None or targetUser is None:
            print("User not found.")
            return False

        user.swipe(targetUserId, action)

        # Check if it's a match
        if action == SwipeAction.RIGHT and targetUser.hasLiked(userId):
            # It's a match!
            chatRoomId = userId + "_" + targetUserId
            chatRoom = ChatRoom(chatRoomId, userId, targetUserId)
            self.chatRooms.append(chatRoom)

            # Notify both users
            NotificationService.getInstance().notifyUser(
                userId, "You have a new match with " + targetUser.getProfile().getName() + "!")
            NotificationService.getInstance().notifyUser(
                targetUserId, "You have a new match with " + user.getProfile().getName() + "!")
            return True
        return False

    def getChatRoom(self, user1Id, user2Id):
        for chatRoom in self.chatRooms:
            if chatRoom.hasParticipant(user1Id) and chatRoom.hasParticipant(user2Id):
                return chatRoom
        return None

    def sendMessage(self, senderId, receiverId, content):
        chatRoom = self.getChatRoom(senderId, receiverId)
        if chatRoom is None:
            print("No chat room found between these users.")
            return

        # Notify the receiver
        chatRoom.addMessage(senderId, content)
        NotificationService.getInstance().notifyUser(
            receiverId, "New message from " + self.getUserById(senderId).getProfile().getName())

    def displayUser(self, userId):
        user = self.getUserById(userId)
        if user is None:
            print("User not found.")
            return
        user.displayProfile()

    def displayChatRoom(self, user1Id, user2Id):
        chatRoom = self.getChatRoom(user1Id, user2Id)
        if chatRoom is None:
            print("No chat room found between these users.")
            return
        chatRoom.displayChat()


# -------------------- Main -------------------- #

class TinderClone:
    @staticmethod
    def main(args):
        # Get the dating app instance
        app = DatingApp.getInstance()

        # Create users
        user1 = app.createUser("user1")
        user2 = app.createUser("user2")

        # Set user1 profile
        profile1 = user1.getProfile()
        profile1.setName("Rohan")
        profile1.setAge(28)
        profile1.setGender(Gender.MALE)
        profile1.setBio("I am a software developer")
        profile1.addPhoto("rohan_photo1.jpg")
        profile1.addInterest("Coding", "Programming")
        profile1.addInterest("Travel", "Lifestyle")
        profile1.addInterest("Music", "Entertainment")

        # Setup user1 preferences
        pref1 = user1.getPreference()
        pref1.addGenderPreference(Gender.FEMALE)
        pref1.setAgeRange(25, 30)
        pref1.setMaxDistance(10.0)
        pref1.addInterest("Coding")
        pref1.addInterest("Travel")

        # Setup user2 profile
        profile2 = user2.getProfile()
        profile2.setName("Neha")
        profile2.setAge(27)
        profile2.setGender(Gender.FEMALE)
        profile2.setBio("Art teacher who loves painting and traveling.")
        profile2.addPhoto("neha_photo1.jpg")
        profile2.addInterest("Painting", "Art")
        profile2.addInterest("Travel", "Lifestyle")
        profile2.addInterest("Music", "Entertainment")

        # Setup user2 preferences
        pref2 = user2.getPreference()
        pref2.addGenderPreference(Gender.MALE)
        pref2.setAgeRange(27, 30)
        pref2.setMaxDistance(15.0)
        pref2.addInterest("Coding")
        pref2.addInterest("Movies")

        # Set location for user1
        location1 = Location()
        location1.setLatitude(1.01)
        location1.setLongitude(1.02)
        profile1.setLocation(location1)

        # Set location for user2 (Close to user1, within 5km)
        location2 = Location()
        location2.setLatitude(1.03)
        location2.setLongitude(1.04)
        profile2.setLocation(location2)

        # Display user profiles
        print("---- User Profiles ----")
        app.displayUser("user1")
        app.displayUser("user2")

        # Find nearby users for user1 (within 5km)
        print("\n---- Nearby Users for user1 (within 5km) ----")
        nearbyUsers = app.findNearbyUsers("user1", 5.0)
        print("Found " + str(len(nearbyUsers)) + " nearby users")
        for user in nearbyUsers:
            print("- " + user.getProfile().getName() + " (" + user.getId() + ")")

        # User1 swipes right on User2
        print("\n---- Swipe Actions ----")
        print("User1 swipes right on User2")
        app.swipe("user1", "user2", SwipeAction.RIGHT)

        # User2 swipes right on User1 (creating a match)
        print("User2 swipes right on User1")
        app.swipe("user2", "user1", SwipeAction.RIGHT)

        # Send messages in the chat room
        print("\n---- Chat Room ----")
        app.sendMessage("user1", "user2", "Hi Neha, Kaise ho?")

        app.sendMessage("user2", "user1", "Hi Rohan, Ma bdiya tum btao")

        # Display the chat room
        app.displayChatRoom("user1", "user2")


if __name__ == "__main__":
    TinderClone.main([])
