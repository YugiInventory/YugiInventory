import React, { useState, useEffect } from "react";
import {
  ActivityIndicator,
  View,
  Text,
  Image,
  FlatList,
  StyleSheet,
  Button,
  TextInput,
} from "react-native";
import { cardSearch, inventoryCardSearch } from "../utility";
import {
  login,
  BASE_URL_,
  getUserId,
  isTokenExpired,
} from "../services/AuthFunctions";
import PaginationBar from "../services/Pagination";
import * as SecureStore from "expo-secure-store";

const Inventory = () => {
  const [allCards, setAllCards] = useState({ cards: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [card, setCard] = useState("");
  // Search bar results
  const [searchData, setSearchData] = useState([]);
  // Create Search Bar
  // Create function searching by card name or ID (handle in request??)
  // Update state with user input
  // Use state to update search params

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const token = await SecureStore.getItemAsync("accessToken");
        // console.log(token);
        // const isExpired = await isTokenExpired();
        // console.log(isExpired);
        const response = await fetch(
          `${BASE_URL_}/inventory/getUserInventory`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const data = await response.json();
        // console.log(await getUserId());
        setAllCards(data.cards);
        // console.log(allCards[9].cardinSet.card.attack);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching cards:", error);
        setIsLoading(false);
      }
    };

    fetchCards();
  }, []);

  const changeText = (e) => {
    // console.log(e);
    setCard(e);
  };

  const handleSearch = async () => {
    if (card.length === 0) {
      console.log("please enter a valid value");
      return null;
    }
    console.log(card);
    const data = await inventoryCardSearch(card);
    if (data === null) {
      console.log("No Cards Found!");
    } else {
      // console.log(data.cards);
      setSearchData(data.cards);
    }
    setCard("");
  };

  const QuantityModal = () => {
    return (
      <View>
        <Button title="add" />
        <Text style={styles.quantityCount}>0</Text>
        <Button title="remove" />
      </View>
    );
  };
  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Image
        source={{ uri: item.cardinSet.card.card_image }}
        style={styles.cardImage}
      />
      <View style={styles.cardInfo}>
        <Text style={styles.cellName}>{item.cardinSet.card.name}</Text>
        <Text style={styles.cell}>
          {item.card_race} {item.cardinSet.card.card_type}
        </Text>
        {item.cardinSet.card.card_type === "Monster" && (
          <View style={styles.statsContainer}>
            <Text style={styles.cell}>
              ATK: {item.cardinSet.card.attack} DEF:{" "}
              {item.cardinSet.card.defense}
            </Text>
          </View>
        )}
        <Text style={styles.cellDescription} numberOfLines={2}>
          {item.cardinSet.card.description}
        </Text>
      </View>
      <QuantityModal />
    </View>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator
          testID="loading-indicator"
          size="large"
          color="#6AB7E2"
        />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.headerTop}>
        <Text style={styles.headerTopText}>Inventory</Text>
      </View>
      <View style={styles.header}>
        <Text style={styles.heading}>Find a Card</Text>
        <TextInput
          value={card}
          onChangeText={changeText}
          placeholder="Find a card"
        />
        <Button title="Search" onPress={handleSearch} />
      </View>
      <FlatList
        // All cards in pool
        data={searchData.length > 0 ? searchData : allCards}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <Text style={styles.emptyText}>No cards found</Text>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: 30,
    paddingHorizontal: 30,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
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
    marginVertical: 8,
    marginHorizontal: 2,
    elevation: 1,
    borderRadius: 3,
    borderColor: "#fff",
    padding: 10,
    backgroundColor: "#fff",
  },
  cardImage: {
    width: 60,
    height: 90,
    marginRight: 10,
  },
  cardInfo: {
    flex: 1,
  },
  cell: {
    fontSize: 14,
    marginBottom: 2,
  },
  cellName: {
    fontWeight: "bold",
    fontSize: 16,
    marginBottom: 5,
  },
  cellDescription: {
    fontSize: 12,
    color: "#666",
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 5,
  },
  emptyText: {
    textAlign: "center",
    marginTop: 20,
    fontSize: 16,
    color: "#666",
  },
  quantityCount: {
    textAlign: "center",
  },
});

export default Inventory;