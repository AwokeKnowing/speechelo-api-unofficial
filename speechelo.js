function say(text)
{
    return postSpeech(text).then(_=>playSpeech())
}


function postSpeech(text)
{
    //rosie
    let data = {
        "languageSelected":"en-US",
        "engineSelected":"neural",
        "voiceSelected":"Salli",
        "toneSelected":"normal",
        "text":text,
        "charCount":text.length,
        "wordsCount":text.split(/\S+/g).length - 1,
        "campaignId":"12345"
    }

    let body = "data="+encodeURIComponent(JSON.stringify(data)).replace('%20','+')



    return fetch("https://app.blasteronline.com/speechelo/blastVoice",{
        method:'post',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Connection': 'keep-alive',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: body
    }).then(r=>r.json())
}

function playSpeech()
{
    fetch("https://app.blasteronline.com/speechelo/getMyBlasters/?_="+Date.now(),{
        method:'get',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Connection': 'keep-alive',
          'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(r=>r.json()).then(response => {
        let link = response.data[response.data.length-1].download_link
        new Audio(link).play()
    })
}

function logIn(user, pass)
{
    let body=`email=${encodeURIComponent(user)}&password=${encodeURIComponent(pass)}`

    return fetch("https://app.blasteronline.com/user/authenticate",{
        method:'post',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Connection': 'keep-alive',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: body
    }).then(r=>r.json())
}


