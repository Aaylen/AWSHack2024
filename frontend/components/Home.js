// Home.js
import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { auth } from './firebaseConfig';

export default function Home({ navigation }) {

    const handleLogout = () => {
        auth.signOut()
            .then(() => {
                navigation.replace('Login');
            })
            .catch(error => console.log(error));
    };

    return (
        <View style={styles.container}>
            <Text>Welcome to the Home Screen!</Text>
            <Button title="Logout" onPress={handleLogout} />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});