import { Button, Text, TextInput, StyleSheet, View } from "react-native";
import {useState} from 'react';
import { BASE_URL } from "../index";


export default function CardInfo() {
    const randomCard = async (cardId = 10) => {
        const card = await fetch(`BASE_URL/card/${cardId}`)
        return (
            <View>
                <h1>{card.name}</h1>
            </View>
        )
    }
    return (
    <View>
        <Button title="Get Information" onPress={() => randomCard(10)}>Get Information</Button>
    </View>
);
}

const styles = StyleSheet.create({
    container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    },
});  