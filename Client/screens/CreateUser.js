import { Button, Text, TextInput, StyleSheet, View } from "react-native"

export default function CreateUser() {
  return (
    <View>
      <TextInput text="Enter Username" />
      <TextInput text="Enter Password" />
      <TextInput text="Confirm Password" />
      <Button title="Create User" />
    </View>
  )
}
