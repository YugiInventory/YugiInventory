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
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
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

const sideDeck = [
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
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

const extraDeck = [
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
  <CardInfo />,
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

const renderItem = ({ item }) => {
  return (
    <View style={styles.itemContainer}>
      <Text style={styles.itemText}>{item}</Text>
    </View>
  );

  // const Table = () => {
  //   const renderItem = ({ item }) => {
  //     return (
  //       <View style={styles.itemContainer}>
  //         <Text style={styles.itemText}>{item}</Text>
  //       </View>
  //     );
  //   };

  //   return (
  //     <FlatList
  //       data={mainDeck}
  //       renderItem={renderItem}
  //       keyExtractor={(item, index) => index.toString()}
  //       numColumns={numColumns}
  //       columnWrapperStyle={styles.row}
  //     />
  //   );
};

const Decks = () => {
  return (
    <View style={styles.container}>
      <View>
        <Text>Main Deck: {mainDeck.length}</Text>
        <FlatList
          data={mainDeck}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
        />
        <Text>Side Deck: {sideDeck.length}</Text>
        <FlatList
          data={sideDeck}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
        />
        <Text>Extra Deck: {extraDeck.length}</Text>
        <FlatList
          data={extraDeck}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          numColumns={numColumns}
          columnWrapperStyle={styles.row}
        />
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
