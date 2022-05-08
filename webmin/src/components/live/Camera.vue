<template>
    <div class="panel panel-default position-relative">
        <video
            class="rounded centered"
            :ref="opaqueId"
            width="100%"
            height="100%"
            autoplay
            playsinline
        ></video>
        <div class="position-absolute" style="top: 5px; right: 5px">
            <i @click="restart" class="fa fa-fw far fa-undo-alt pointer"></i>
        </div>
        <div v-if="false" class="d-flex flex-row">
            <span v-if="showBitrate" class="label label-primary">{{bitrate}}</span>
            <span v-if="showResolution" class="label label-info">{{resolutionWidth}}x{{resolutionHeight}}</span>
        </div>
    </div>
</template>

<script>
import Janus from '@/janus.js'
import roomStore from "@/store/roomStore.js"

export default {
    name: 'Camera',
    data() {
        return {
            url: undefined,
            streamId: undefined,
            opaqueId: null,
            janus: null,
            streamingPlugin: null,
            bitrate: 0,
            showBitrate: false,
            resolutionHeight: 0,
            resolutionWidth: 0,
            showResolution: false,
            bitrateTimer: null,
        }
    },
    computed: {
        roomDefaultChannel() {
            for (let room of roomStore.state.rooms) {
                if (room.id === this.roomId) {
                return room.default_publication_channel
                }
            }

            // Can never happen, because roomStore.state.rooms is always defined if this component exist
            // This return statement just fixes a Vue compilation error
            return 'default_channel'
        },
    },
    methods: {
        restart() {
            const paramsObject = JSON.parse(this.params)
            roomStore.dispatch(
                'widgetAction',
                {channel: this.roomDefaultChannel, widgetId: "camera-" + paramsObject.channel, widgetType: 'camera', action: "restart", 'camera_id': paramsObject.id}
            )
        },
        initialize() {
            this.janus = new Janus(
                {
                    server: this.url,
                    success: this.janusSuccessCallback,
                    error: function(error) {
                        Janus.error(error)
                    },
                    destroyed: function() {
                        Janus.error("Janus was unexpectedly destroyed")
                    }
                }
            )
        },
        janusSuccessCallback() {
            this.janus.attach(
                {
                    plugin: "janus.plugin.streaming",
                    opaqueId: this.opaqueId,
                    success: this.janusStreamingSuccessCallback,
                    error: function(error) {
                        Janus.error("  -- Error attaching plugin... ", error)
                    },
                    iceState: function(state) {
                        Janus.log("ICE state changed to " + state)
                    },
                    webrtcState: function(on) {
                        Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now")
                    },
                    onmessage: this.janusStreamingOnmessageCallback,
                    onremotestream: this.janusStreamingOnremotestreamCallback,
                    /* eslint-disable-next-line */
                    ondataopen: function(data) {
                        // The data channel is available
                    },
                    /* eslint-disable-next-line */
                    ondata: function(data) {
                        // data received from the data channel
                    },
                    oncleanup: this.janusOncleanupCallback,
                }
            )
        },
        janusStreamingSuccessCallback(pluginHandle) {
            this.streamingPlugin = pluginHandle
            this.streamingPlugin.send({message: {request: "watch", id: this.streamId}})
        },
        janusStreamingOnmessageCallback(msg, jsep) {
            if(msg["error"] || msg["result"] && msg["result"]["status"] && msg["result"]["status"] === 'stopped') {
                this.stopStream()
                return
            }
            if(jsep) {
                var stereo = (jsep.sdp.indexOf("stereo=1") !== -1)
                // Offer from the plugin, let's answer
                // streamingPlugin = this.streamingPlugin
                this.streamingPlugin.createAnswer(
                    {
                        jsep: jsep,
                        // We want recvonly audio/video and no datachannels
                        media: {audioSend: false, videoSend: false, data: false},
                        customizeSdp: function(jsep) {
                            if(stereo && jsep.sdp.indexOf("stereo=1") == -1) {
                                // Make sure that our offer contains stereo too
                                jsep.sdp = jsep.sdp.replace("useinbandfec=1", "useinbandfec=1;stereo=1")
                            }
                        },
                        success: this.janusStreamingSDPSuccessCallback,
                        error: function(error) {
                            Janus.error("WebRTC error:", error)
                        }
                    }
                )
            }
        },
        janusStreamingSDPSuccessCallback(jsep) {
            this.streamingPlugin.send({message: {request: "start"}, jsep: jsep})
        },
        janusStreamingOnremotestreamCallback(stream) {
            Janus.attachMediaStream(this.$refs[this.opaqueId], stream)

            this.showBitrate = true
            this.bitrateTimer = setInterval(function(this_) {
                this_.bitrate = this_.streamingPlugin.getBitrate()
                // Check if the resolution changed too
                this_.resolutionWidth = this_.$refs[this_.opaqueId].videoWidth
                this_.resolutionHeight = this_.$refs[this_.opaqueId].videoHeight
                if(this_.resolutionWidth > 0 && this_.resolutionHeight > 0)
                    this_.showResolution = true
            }, 1000, this)
        },
        janusStreamingOncleanupCallback() {
            this.showBitrate = false
            this.showResolution = false
            clearInterval(this.bitrateTimer)
        },
        stopStream() {
            this.streamingPlugin.send({message: {request: "stop"}})
            this.streamingPlugin.hangup()
            clearInterval(this.bitrateTimer)
        },
    },
    mounted() {
        const paramsObject = JSON.parse(this.params)
        this.url = paramsObject.url
        this.streamId = paramsObject.streamId

        this.opaqueId = "streaming-" + Janus.randomString(12)
        Janus.init({debug: false, callback: this.initialize})
    },
    props: {
        params: String,
        roomId: Number,
    }
}
</script>