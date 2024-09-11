import React, { useEffect,useState } from "react";
import * as SQlite from 'expo-sqlite';
import { View,Text, Button } from "react-native";

// At its core what is pagination just doing?
//We are just moving saying I want a different batch of data. 
// We can break this down to just having functions that will request data. 
// That can either be in the form of an API call, querying the local DB, etc.
// It would have to be buttons saying +1, -1, Last, First, Jump to 

function createAPIURL(base_url,filter_obj){
    //return the path 
    const url = URL(base_url);
    Object.entries(filter_obj).forEach(([key,value]) => {
        if (value!==undefined && value!==null){
            url.searchParams.append(key,value)
        }
    })
    console.log(url.toString())
    return url.toString()
}


async function getPageDatafromAPI(path,newPage){
    access_token = ''
    try {
        const resp = await fetch(`${path}&page=${newPage}`);
        if (resp.ok) {
            const data = await resp.json() //this is a promise not the value;
            return data
        } else {
            console.log('error getting cards')
            return null
        }
    } catch (error) {
        console.log('Error:',error)
        return null
    }
}

function buildSQLQuery(tablename, columns = ['*'], filters = {}, orderby=null, limit=null, offset=0 ){
    //need to know what table to query, what filters, limit = per_page, and offset=for the page number*per_page
    //SELECT COLUMNS FROM TABLENAME WHERE CONDITIONS LIMIT limitval OFFSET offsetval
    let query = `SELECT ${columns.join(', ')} FROM ${tablename}}`;
    return query
}

function getPageDatafromLocal(){
    //This would be getting the data from the local sqlite database.
    //We would need to prepare a query from the filters.
    //pass that query to the database and get the output.
    //from the output either use limits to get certain values or return the cards and then manually choose what to render and use offset to keep track of where in the list of cards we are. 
    buildSQLQuery()
    //execute the query, return results
}

function PaginationBar ({currentPage,setCurrentPage,lastPage,cardsPerPage,totalCards,getDatafcn}){
    console.log('???')

    function handlePress(offset){
        //Get New Data
        //Get offset so we can get the values which is the value saved in the button. some have -1,+1, 1-current, last - current, 0. This says which page to get. For db queries I would guess that we can just use this to move the cursor to a different location.
        //Use this value to get the  
        const newPage = currentPage + offset      
        if (newPage !== currentPage){
            //some function to get the data and return it, should also have information on the currentPage information
            getDatafcn()  //let this function handle setting the state in the parent
            .then((data) => {
                if (data) {
                    setCurrentPage(newPage); 
                }
            })
            .catch((error)=>console.log(error)) //getData is returning a promise so catch for the error. 
        }
    }
    return(
        <View>
            <Button title='First Page' disabled={currentPage===1} onPress={handlePress(offset=(1-currentPage))}></Button>
            <Button title="Previous Page" disabled={currentPage===1} onPress={handlePress(offset=-1)}></Button>
            <Button title="Current Page" disabled></Button>
            <Button title="Next Page" disabled= {(currentPage+1>lastPage)} onPress={handlePress(offset=1)}></Button>
            <Button title="Last Page" disabled={currentPage===lastPage} onPress={handlePress(offset=(lastPage-currentPage))}></Button>
        </View>
    )
}

export default PaginationBar

{/* <Text>Page: {currentPage} of {lastPage}</Text>
<View>
    <button disabled={currentPage===1} onClick={handleClick} value={1-currentPage}><Text>First Page</Text> </button>
    <button disabled= {currentPage===1} onClick={handleClick} value={-1}><Text>Prev Page</Text></button>
    <button disabled><Text>Current Page</Text></button>
    <button disabled= {(currentPage+1>lastPage)} onClick={handleClick} value={1}><Text>Next Page</Text></button>
    <button disabled={currentPage===lastPage} onClick={handleClick} value={lastPage-currentPage}><Text>Last Page</Text></button>
</View>
<Text>Showing: {(currentPage-1)*cardsPerPage + 1}-{Math.min(currentPage*cardsPerPage,totalCards)} of {totalCards}</Text> */}