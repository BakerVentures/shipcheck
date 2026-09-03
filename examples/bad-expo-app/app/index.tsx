import { View, Text, Button } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency';
import * as Location from 'expo-location';
import { GoogleSignin } from '@react-native-google-signin/google-signin';
import { LoginManager } from 'react-native-fbsdk-next';
import Purchases from 'react-native-purchases';
import { supabase } from '../lib/supabase';

export default function Home() {
  const [permission, requestPermission] = useCameraPermissions();

  async function addPhoto() {
    await ImagePicker.launchCameraAsync({ quality: 0.8 });
    await ImagePicker.launchImageLibraryAsync();
  }

  async function trackMe() {
    await requestTrackingPermissionsAsync();
  }

  async function whereAmI() {
    await Location.requestForegroundPermissionsAsync();
    await Location.getCurrentPositionAsync({});
  }

  return (
    <View>
      <Text>Welcome</Text>
      <CameraView facing="back" />
      <Button title="Add photo" onPress={addPhoto} />
      <Button title="Personalize ads" onPress={trackMe} />
      <Button title="Find gyms near me" onPress={whereAmI} />
      <Button title="Sign in with Google" onPress={() => GoogleSignin.signIn()} />
      <Button title="Continue with Facebook" onPress={() => LoginManager.logInWithPermissions(['email'])} />
      <Button title="Go Pro" onPress={() => Purchases.purchasePackage(pkg)} />
    </View>
  );
}
