import { launchImageLibrary } from 'react-native-image-picker';
import Geolocation from '@react-native-community/geolocation';

export function App() {
  const pick = () => launchImageLibrary({ mediaType: 'photo' });
  const locate = () => Geolocation.getCurrentPosition(() => {});
  return null;
}
