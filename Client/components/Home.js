import { Button, Text, TextInput, StyleSheet, View } from "react-native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Profile from "./Profile";
import Inventory from "./Inventory";
import Decks from "./Decks";
import Login from "./Login";

const Tab = createBottomTabNavigator();

const Home = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen style={styles.container} name="Profile" component={Profile} />
      <Tab.Screen name="Decks" component={Decks} />
      <Tab.Screen name="Inventory" component={Inventory} />
      <Tab.Screen name="Login" component={Login} />


    </Tab.Navigator>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
  },
});

export default Home;
