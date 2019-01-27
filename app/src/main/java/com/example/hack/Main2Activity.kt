package com.example.hack

import okhttp3.*
import java.io.IOException

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_main2.*


class Main2Activity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)
        fetchXML()

        val Rnum=0
//        num.text="hi"

    }
    fun test(body: String) {
        this@Main2Activity.runOnUiThread(java.lang.Runnable {
            this.num.text=body
        })
//        num.text="omg"
    }
    fun fetchXML() {
        println("Attempting to Fetch JSON")
        //val url = "http://127.0.0.1:5000/get_data"
        val url = "http://10.0.2.2:5000/get_data?file_name=sample_3.wav"
        //  url = "https://api.letsbuildthatapp.com/youtube/home_feed"
        //val url = "https://www.w3schools.com/xml/note.xml"

        val request = Request.Builder().url(url).build()

        val client = OkHttpClient()
        //println("here 1111")
        client.newCall(request).enqueue(object: Callback {
            override fun onResponse(call: Call, response: Response) {
                //println("here 1111")
                val body = response.body()?.string()
                //println("!!!!!!!!!!!!!!!!!" + body)
                test(body.toString())

            }
            override fun onFailure(call: Call, e: IOException) {
                //println("${e?.message}")
            }
        })
        //return ("3")
        //num.text="omg"
    }
}
