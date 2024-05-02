import React from "react";
import { Text, TextInput, StyleSheet, View, Button } from "react-native";
import { BASE_URL } from "../index";
import { useForm, Controller } from "react-hook-form";
import CardInfo from "./CardInfo";

export default function Login({ navigation }) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      username: "",
      password: "",
    },
  });
  const onSubmit = async (data) => {
    const user = await fetch(`${BASE_URL}/user`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: user.username,
        password: user.password,
        email: null,
      }),
    }).then((response) => {
      const res = response.json();
      console.log(res);
      if (data.username === user.username && data.password === user.password) {
        navigation.navigate("Home")
      } else {
        console.log(data, 'data')
        console.log("Login information incorrect")
      }
    });
  };


  // const handleLogin = () => {
  //   navigation.navigate("Home");
  // };

  const handleCreateUserScreen = () => {
    navigation.navigate("CreateUser");
  };

  return (
    <View>
       <Controller
        control={control}
        rules={{
          required: true,
        }}
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            placeholder="Username"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
          />
        )}
        name="username"
      />
      {errors.username && <Text>This is required.</Text>}

      <Controller
        control={control}
        rules={{
          required: true,
        }}
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            placeholder="Password"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
          />
        )}
        name="passowrd"
      />
      {errors.password && <Text>This is required.</Text>}

      <Button title="Login" onPress={handleSubmit(onSubmit)} />

      <View style={styles.buttonSuite}>
        <Button title="Create User" onPress={handleCreateUserScreen} />
      </View>
      {/* <Text>Placeholder for Logo</Text>
      <View style={styles.container}>
        <TextInput placeholder="Username" />
        <TextInput placeholder="Password" />
        <CardInfo />
      </View> */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
  },
  buttonSuite: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  buttons: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 4,
    elevation: 3,
    backgroundColor: "#2196f3",
    color: "white",
  },
});
