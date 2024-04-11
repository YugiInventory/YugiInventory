import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import Profile from './screens/Profile';
import Settings from './screens/Settings';
import Decks from './screens/Decks';
import Inventory from './screens/Inventory';
import Login from './screens/Login'

const Tab = createBottomTabNavigator()

// function HomeScreen() {
//   return (
//     <Tab.Navigator>
//     <View style={styles.container}>
//       <Text>Yugi Inventory</Text>
//       <StatusBar style='auto' />
//     </View>
//     </Tab.Navigator>
//   );
// }

const Stack = createNativeStackNavigator();

// export default function App() {
//   return (
//     <NavigationContainer>
//       <Stack.Navigator>
//         <Stack.Screen name='Home' component={HomeScreen} />
//       </Stack.Navigator>
//     </NavigationContainer>
//   );
// }

// Login Page must be first screen users encounter

function Home() {
  return (
    <Tab.Navigator>
      <Tab.Screen style={styles.container} name="Profile" component={Profile} />
      <Tab.Screen name="Decks" component={Decks} />
      <Tab.Screen name="Inventory" component={Inventory} />
      <Tab.Screen name="Settings" component={Settings} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Login/>
        {/* <Stack.Screen
          name="Home"
          component={Home}
          options={{ headerShown: false }}
          />
        <Stack.Screen name="Profile" component={Profile} />
        <Stack.Screen name="Settings" component={Settings} /> */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});