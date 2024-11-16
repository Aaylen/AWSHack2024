// Login.js
import React, { useState } from 'react';
import { auth, googleProvider } from './firebaseConfig';
import {
    View,
    Text,
    TextInput,
    Button,
    StyleSheet,
    Alert
} from 'react-native';

export default function Login({ navigation }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = () => {
        auth.signInWithEmailAndPassword(email, password)
            .then(userCredentials => {
                const user = userCredentials.user;
                Alert.alert('Login successful', `Welcome ${user.email}`);
                navigation.replace('Home');
            })
            .catch(error => Alert.alert('Login failed', error.message));
    };

    const handleGoogleLogin = () => {
        auth.signInWithPopup(googleProvider)
            .then(result => {
                const user = result.user;
                Alert.alert('Login successful', `Welcome ${user.email}`);
                navigation.replace('Home');
            })
            .catch(error => Alert.alert('Google Sign-In failed', error.message));
    };

    return (
        <View style={styles.container}>
            <Text>Login</Text>
            <TextInput
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                style={styles.input}
            />
            <TextInput
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                style={styles.input}
            />
            <Button title="Login" onPress={handleLogin} />
            <Button title="Login with Google" onPress={handleGoogleLogin} />
            <Button
                title="Register"
                onPress={() => navigation.navigate('Register')}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 16,
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        marginBottom: 12,
        padding: 10,
    },
});