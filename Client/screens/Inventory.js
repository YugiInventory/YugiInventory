import React, { useState, useEffect } from "react";
import {
  ActivityIndicator,
  View,
  Text,
  Image,
  FlatList,
  StyleSheet,
  Button,
} from "react-native";
import BASE_URL from "../config";

const Inventory = () => {
  const [allCards, setAllCards] = useState({ cards: [] });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const response = await fetch(`${BASE_URL}/cards`);
        const data = await response.json();
        // console.log(data);
        setAllCards(data);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching cards:", error);
        setIsLoading(false);
      }
    };

    fetchCards();
  }, []);

  const QuantityModal = () => {
    return (
      <View>
        <Button title="+" />
        <Text style={styles.quantityCount}>0</Text>
        <Button title="-" />
      </View>
    );
  };
  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Image source={{ uri: item.card_image }} style={styles.cardImage} />
      <View style={styles.cardInfo}>
        <Text style={styles.cellName}>{item.name}</Text>
        <Text style={styles.cell}>
          {item.card_race} {item.card_type}
        </Text>
        {item.card_type === "Monster" && (
          <View style={styles.statsContainer}>
            <Text style={styles.cell}>
              ATK: {item.attack} DEF: {item.defense}
            </Text>
          </View>
        )}
        <Text style={styles.cellDescription} numberOfLines={2}>
          {item.description}
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
      </View>
      <FlatList
        data={allCards.cards}
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
