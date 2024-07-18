import React from "react";
import { Button, FlatList, StyleSheet, Text, TextInput, View } from "react-native";
import BASE_URL from "../index";
import {login} from '../services/AuthFunctions'


const data = [
  { id: 1, name: "Blackwing Shura", atk: "1800", def: "1200", quantity: 0 },
  { id: 2, name: "Blackwing Gale", atk: "1300", def: "400", quantity: 0 },
  { id: 3, name: "Blackwing Bora", atk: "1700", def: "800", quantity: 0 },
  { id: 4, name: "Blackwing Sirocco", atk: "2000", def: "900", quantity: 0 },
  { id: 5, name: "Blackwing Vayu", atk: "800", def: "0", quantity: 0 },
  { id: 6, name: "Blackwing Kalut", atk: "1400", def: "1000", quantity: 0 },
  { id: 7, name: "Blackwing Zephyros", atk: "1600", def: "400", quantity: 0 },
  {
    id: 8,
    name: "Blackwing Armor Master",
    atk: "2500",
    def: "1600",
    quantity: 0,
  },
  {
    id: 9,
    name: "Blackwing Armed Wing",
    atk: "2300",
    def: "1000",
    quantity: 0,
  },
  {
    id: 10,
    name: "Blackwing Silverwind",
    atk: "2800",
    def: "2300",
    quantity: 0,
  },
];
const Inventory = () => {
  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.name}</Text>
      <Text style={styles.cell}>{item.atk}</Text>
      <Text style={styles.cell}>{item.def}</Text>
      <Text style={styles.cell}>{item.quantity}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.headerTop}>
        <Text style={styles.headerTopText}>Inventory</Text>
      </View>
      <View style={styles.header}>
        <Text style={styles.heading}>Find a Card</Text>
      </View>
      <FlatList
        data={data}
        keyExtractor={(item) => {
          item.id.toString();
        }}
        renderItem={renderItem}
      />
      <View>
        <TextInput 
        placeholder="Username"
        />
        <TextInput
        placeholder="password"
        />
        <Button title="Login"/>
      </View>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: 30,
    paddingHorizontal: 30,
  },
  headerTop: {
    backgroundColor: "#6AB7E2",
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 5,
    elevation: 2,
    marginBottom: 10,
  },
  headerTopText: {
    color: "#fff",
    fontSize: 16,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    padding: 10,
  },
  heading: {
    flex: 1,
    fontSize: 15,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginVertical: 8,
    marginHorizontal: 2,
    elevation: 1,
    borderRadius: 3,
    borderColor: "#fff",
    padding: 10,
    backgroundColor: "#fff",
  },
  cell: {
    fontSize: 15,
    textAlign: "left",
    flex: 1,
  },
});

export default Inventory;
