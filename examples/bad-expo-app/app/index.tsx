import { View, Text, Button } from 'react-native';
import { GoogleSignin } from '@react-native-google-signin/google-signin';
import { LoginManager } from 'react-native-fbsdk-next';
import Purchases from 'react-native-purchases';
import { supabase } from '../lib/supabase';

export default function Home() {
  return (
    <View>
      <Text>Welcome</Text>
      <Button title="Sign in with Google" onPress={() => GoogleSignin.signIn()} />
      <Button title="Continue with Facebook" onPress={() => LoginManager.logInWithPermissions(['email'])} />
      <Button title="Go Pro" onPress={() => Purchases.purchasePackage(pkg)} />
    </View>
  );
}
