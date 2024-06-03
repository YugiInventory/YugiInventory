import { Text, Button, StyleSheet, View } from "react-native";


const Profile = () => {
  return (
    <View>
      <Text style={styles.container}>Profile</Text>
      <Button>Logout</Button>
    </View>
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

export default Profile;
