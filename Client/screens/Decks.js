import {Text, StyleSheet} from 'react-native';

export default function Decks() {
  return (
    <Text style={styles.container}>Decks</Text>
  )
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
    },
  });