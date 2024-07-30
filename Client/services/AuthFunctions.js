import * as SecureStore from 'expo-secure-store'

const BASE_URL_ = "http://ec2-3-135-192-227.us-east-2.compute.amazonaws.com:8000/";
const BASE_URL = "http://127.0.0.1:5555/"

const storeTokens = async (accessToken, refreshToken) => {
    try {
        await SecureStore.setItemAsync('accessToken', accessToken);
        await SecureStore.setItemAsync('refreshToken', refreshToken)
    }
    catch(e){
        console.error('Error Storing tokens',e)
    }

    await SecureStore.getItemAsync('accessToken').then(result => console.log(result))
};

const clearTokens = async () => {
    try {
        await SecureStore.deleteItemAsync('accessToken');
        await SecureStore.deleteItemAsync('refreshToken')
    }
    catch(e){
        console.log('Error deleting tokens' ,e)
    }
}

const login = async (username, password, rmrFlag) => {

    console.log(JSON.stringify({username,password}))
    console.log(BASE_URL)
    try { 
        // `${BASE_URL}/Login`
        const response = await fetch(`${BASE_URL_}/Login` , {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
            },
            body: JSON.stringify({username, password}),
        });
    
        console.log(response.text)   

    if (!response.ok) {
        console.log('Error?')
        throw new Error('Login failed');
    }

    const data = await response.json();
    const {accessToken, refreshToken} = data;
    
    if (rmrFlag) {
        await storeTokens(accessToken, refreshToken)
    } 
    else {
        await SecureStore.setItemAsync('accessToken', accessToken)
    } return data;
    }

    catch(e){
        console.log('Error Logging in', e);
        throw e;
    }
}

const logout = async () => {
    await clearTokens();
}


export {login, logout, clearTokens, storeTokens}