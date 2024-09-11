import { Text, StyleSheet, View, FlatList, Image } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { useState, useCallback } from "react";

const renderItem = ({ item }) => {
  return (
    <View style={styles.itemContainer}>
      <Image source={{ uri: item.card.card_image }} style={styles.cardImage} />
      <Text style={styles.itemText}>{item.card_name}</Text>
    </View>
  );
};

// Make DECK its own component and map each deck in DECKS screen
// Each CARD in a deck should show quantity and also allow users to view CARD INFO when pressing card

const Decks = () => {
  const [main, setMain] = useState([]);
  const [side, setSide] = useState([]);
  const [extra, setExtra] = useState([]);
  const numColumns = 5;

  const deck = async () => {
    try {
      const response = await fetch(
        "http://ec2-3-135-192-227.us-east-2.compute.amazonaws.com:8000/deck/getSingleDeckCardInfo/1"
      );
      const data = await response.json();
      setMain(data.card_in_deck.filter((card) => card.location === "main"));
      setSide(data.card_in_deck.filter((card) => card.location === "side"));
      setExtra(data.card_in_deck.filter((card) => card.location === "extra"));
      return data;
    } catch (error) {
      console.log("Error fetching deck:", error);
    }
  };

  useFocusEffect(
    useCallback(() => {
      deck(); // Fetch deck data when screen is focused
    }, []) // Empty array to run it only the first time the screen is focused
  );

  return (
    <View style={styles.container}>
      <View>
        <Text>Main Deck: {main.length}</Text>
        <FlatList
          data={main}
          renderItem={renderItem}
          keyExtractor={(item) => item.yg_pro_id}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
          contentContainerStyle={styles.listContainer}
        />
        <Text>Side Deck: {side.length}</Text>
        <FlatList
          data={side}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
          contentContainerStyle={styles.listContainer}
        />
        <Text>Extra Deck: {extra.length}</Text>
        <FlatList
          data={extra}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
          contentContainerStyle={styles.listContainer}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    padding: 10,
  },
  listContainer: {
    alignItems: "flex-start", // Align items from left to right
  },
  row: {
    justifyContent: "flex-start", // Align the items from left to right within each row
    marginVertical: 10,
  },
  itemContainer: {
    width: 75,
    height: 120,
    justifyContent: "center",
    alignItems: "center",
    margin: 0,
    borderRadius: 8,
  },
  cardImage: {
    width: "100%",
    height: "100%",
    resizeMode: "contain", // Ensures the image fits within the container
  },
  itemText: {
    fontSize: 12,
    textAlign: "center",
  },
});

export default Decks;
