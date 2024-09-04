import { Text, StyleSheet, View, FlatList } from "react-native";
import CardInfo from "./CardInfo";

const mainDeck = [
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
];

const numColumns = 5;

const Table = () => {
  const renderItem = ({ item }) => {
    return (
      <View style={styles.itemContainer}>
        <Text style={styles.itemText}>{item}</Text>
      </View>
    );
  };

  return (
    <FlatList
      data={mainDeck}
      renderItem={renderItem}
      keyExtractor={(item, index) => index.toString()}
      numColumns={numColumns}
      columnWrapperStyle={styles.row}
    />
  );
};

const Decks = () => {
  return (
    <View style={styles.container}>
      <View>
        <Text>Main</Text>
        <Table />
      </View>
      <View>
        <Text>Side</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  row: {
    justifyContent: "space-between",
    marginVertical: 10,
  },
  itemContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    margin: 5,
    backgroundColor: "#f9c2ff",
  },
  itemText: {
    fontSize: 16,
  },
});

export default Decks;
