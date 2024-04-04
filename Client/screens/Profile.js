import {Text, StyleSheet} from 'react-native';

export default function Profile() {
  return (
    <Text style={styles.container}>Profile</Text>
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