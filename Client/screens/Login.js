import React, { useState } from "react";
import * as SecureStore from 'expo-secure-store'
import { Text, TextInput, StyleSheet, View, Button } from "react-native";
import BASE_URL from "../index";
import { useForm, Controller } from "react-hook-form";
import CardInfo from "./CardInfo";
import {storeTokens, clearTokens, login} from '../services/AuthFunctions'
import Inventory from "./Inventory";


const Login = () => {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  const [createusername,setcreateusername] = useState('');
  const [createpassword,setcreatepassword] = useState('');
  const [createEmail, setcreateEmail] = useState('');

  const BASE_URL_ = "http://ec2-3-135-192-227.us-east-2.compute.amazonaws.com:8000/";
  const BASE_URL = "http://127.0.0.1:5555/"



  const handleLogin = () => {
    //Login Have the user submit the login credentials. 
    //Get a return back from the server and if it is good then we will also have a refreshToken and an accessToken
    //Store these values in securestore.

    console.log('Username:',username);
    console.log('Password:',password)
    

    login(username,password)

    console.log('haha');
  
    storeTokens('f','f');
  
    console.log('we made it')
  }
  
  const handleLogout = () => {
    console.log('logout');
    clearTokens()
  }

  const handleCreateAccount = async () =>{
    console.log(createusername);
    console.log(createpassword);
    console.log(createEmail)

    //Send post request with the informatin

    try {
      const response = await fetch(`${BASE_URL_}/cards`);
      if (!response.ok){
        throw new Error('???')
      }
      
      const json_out = await response.json();
      console.log(json_out);

    }
    catch (e){
      console.log(e.message)
    }


  }



  return (
    <View>
      <TextInput placeholder="username" onChangeText={setUsername}/>
      <TextInput secureTextEntry={true} placeholder="password" onChangeText={setPassword} />

      <View style={styles.buttonSuite}>
        <Button title="Login" onPress={handleLogin} />
        <Button title="Logout" onPress={handleLogout} />
      </View> 

      <View>
          <TextInput placeholder="Create Username" onChangeText={setcreateusername}/>
          <TextInput placeholder="Create Strong Password" onChangeText={setcreatepassword}/>
          <TextInput placeholder="enter email" onChangeText={setcreateEmail} />
          <Button title="Create Account" onPress={handleCreateAccount}/>         
      </View>
    </View>

  );
};

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

export default Login;
