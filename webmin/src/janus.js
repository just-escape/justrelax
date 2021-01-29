/* eslint-disable */
/*
	The MIT License (MIT)

	Copyright (c) 2016 Meetecho

	Permission is hereby granted, free of charge, to any person obtaining
	a copy of this software and associated documentation files (the "Software"),
	to deal in the Software without restriction, including without limitation
	the rights to use, copy, modify, merge, publish, distribute, sublicense,
	and/or sell copies of the Software, and to permit persons to whom the
	Software is furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included
	in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
	OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
	THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
	ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
	OTHER DEALINGS IN THE SOFTWARE.
 */

// https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/6.4.0/adapter.min.js
!function(e){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{("undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this).adapter=e()}}(function(){return function a(o,s,c){function d(t,e){if(!s[t]){if(!o[t]){var r="function"==typeof require&&require;if(!e&&r)return r(t,!0);if(p)return p(t,!0);var n=new Error("Cannot find module '"+t+"'");throw n.code="MODULE_NOT_FOUND",n}var i=s[t]={exports:{}};o[t][0].call(i.exports,function(e){return d(o[t][1][e]||e)},i,i.exports,a,o,s,c)}return s[t].exports}for(var p="function"==typeof require&&require,e=0;e<c.length;e++)d(c[e]);return d}({1:[function(e,t,r){"use strict";var N=e("sdp");function c(e,t,r,n,i){var a=N.writeRtpDescription(e.kind,t);if(a+=N.writeIceParameters(e.iceGatherer.getLocalParameters()),a+=N.writeDtlsParameters(e.dtlsTransport.getLocalParameters(),"offer"===r?"actpass":i||"active"),a+="a=mid:"+e.mid+"\r\n",e.rtpSender&&e.rtpReceiver?a+="a=sendrecv\r\n":e.rtpSender?a+="a=sendonly\r\n":e.rtpReceiver?a+="a=recvonly\r\n":a+="a=inactive\r\n",e.rtpSender){var o=e.rtpSender._initialTrackId||e.rtpSender.track.id;e.rtpSender._initialTrackId=o;var s="msid:"+(n?n.id:"-")+" "+o+"\r\n";a+="a="+s,a+="a=ssrc:"+e.sendEncodingParameters[0].ssrc+" "+s,e.sendEncodingParameters[0].rtx&&(a+="a=ssrc:"+e.sendEncodingParameters[0].rtx.ssrc+" "+s,a+="a=ssrc-group:FID "+e.sendEncodingParameters[0].ssrc+" "+e.sendEncodingParameters[0].rtx.ssrc+"\r\n")}return a+="a=ssrc:"+e.sendEncodingParameters[0].ssrc+" cname:"+N.localCName+"\r\n",e.rtpSender&&e.sendEncodingParameters[0].rtx&&(a+="a=ssrc:"+e.sendEncodingParameters[0].rtx.ssrc+" cname:"+N.localCName+"\r\n"),a}function A(d,p){var u={codecs:[],headerExtensions:[],fecMechanisms:[]},f=function(e,t){e=parseInt(e,10);for(var r=0;r<t.length;r++)if(t[r].payloadType===e||t[r].preferredPayloadType===e)return t[r]};return d.codecs.forEach(function(r){for(var e=0;e<p.codecs.length;e++){var t=p.codecs[e];if(r.name.toLowerCase()===t.name.toLowerCase()&&r.clockRate===t.clockRate){if("rtx"===r.name.toLowerCase()&&r.parameters&&t.parameters.apt&&(n=r,i=t,a=d.codecs,o=p.codecs,c=s=void 0,s=f(n.parameters.apt,a),c=f(i.parameters.apt,o),!s||!c||s.name.toLowerCase()!==c.name.toLowerCase()))continue;(t=JSON.parse(JSON.stringify(t))).numChannels=Math.min(r.numChannels,t.numChannels),u.codecs.push(t),t.rtcpFeedback=t.rtcpFeedback.filter(function(e){for(var t=0;t<r.rtcpFeedback.length;t++)if(r.rtcpFeedback[t].type===e.type&&r.rtcpFeedback[t].parameter===e.parameter)return!0;return!1});break}}var n,i,a,o,s,c}),d.headerExtensions.forEach(function(e){for(var t=0;t<p.headerExtensions.length;t++){var r=p.headerExtensions[t];if(e.uri===r.uri){u.headerExtensions.push(r);break}}}),u}function a(e,t,r){return-1!=={offer:{setLocalDescription:["stable","have-local-offer"],setRemoteDescription:["stable","have-remote-offer"]},answer:{setLocalDescription:["have-remote-offer","have-local-pranswer"],setRemoteDescription:["have-local-offer","have-remote-pranswer"]}}[t][e].indexOf(r)}function U(e,t){var r=e.getRemoteCandidates().find(function(e){return t.foundation===e.foundation&&t.ip===e.ip&&t.port===e.port&&t.priority===e.priority&&t.protocol===e.protocol&&t.type===e.type});return r||e.addRemoteCandidate(t),!r}function m(e,t){var r=new Error(t);return r.name=e,r.code={NotSupportedError:9,InvalidStateError:11,InvalidAccessError:15,TypeError:void 0,OperationError:void 0}[e],r}t.exports=function(I,L){function j(e,t){t.addTrack(e),t.dispatchEvent(new I.MediaStreamTrackEvent("addtrack",{track:e}))}function i(e,t,r,n){var i=new Event("track");i.track=t,i.receiver=r,i.transceiver={receiver:r},i.streams=n,I.setTimeout(function(){e._dispatchEvent("track",i)})}var n=function(e){var t,n,i,r=this,a=document.createDocumentFragment();if(["addEventListener","removeEventListener","dispatchEvent"].forEach(function(e){r[e]=a[e].bind(a)}),this.canTrickleIceCandidates=null,this.needNegotiation=!1,this.localStreams=[],this.remoteStreams=[],this._localDescription=null,this._remoteDescription=null,this.signalingState="stable",this.iceConnectionState="new",this.connectionState="new",this.iceGatheringState="new",e=JSON.parse(JSON.stringify(e||{})),this.usingBundle="max-bundle"===e.bundlePolicy,"negotiate"===e.rtcpMuxPolicy)throw m("NotSupportedError","rtcpMuxPolicy 'negotiate' is not supported");switch(e.rtcpMuxPolicy||(e.rtcpMuxPolicy="require"),e.iceTransportPolicy){case"all":case"relay":break;default:e.iceTransportPolicy="all"}switch(e.bundlePolicy){case"balanced":case"max-compat":case"max-bundle":break;default:e.bundlePolicy="balanced"}if(e.iceServers=(t=e.iceServers||[],n=L,i=!1,(t=JSON.parse(JSON.stringify(t))).filter(function(e){if(e&&(e.urls||e.url)){var t=e.urls||e.url;e.url&&!e.urls&&console.warn("RTCIceServer.url is deprecated! Use urls instead.");var r="string"==typeof t;return r&&(t=[t]),t=t.filter(function(e){return 0!==e.indexOf("turn:")||-1===e.indexOf("transport=udp")||-1!==e.indexOf("turn:[")||i?0===e.indexOf("stun:")&&14393<=n&&-1===e.indexOf("?transport=udp"):i=!0}),delete e.url,e.urls=r?t[0]:t,!!t.length}})),this._iceGatherers=[],e.iceCandidatePoolSize)for(var o=e.iceCandidatePoolSize;0<o;o--)this._iceGatherers.push(new I.RTCIceGatherer({iceServers:e.iceServers,gatherPolicy:e.iceTransportPolicy}));else e.iceCandidatePoolSize=0;this._config=e,this.transceivers=[],this._sdpSessionId=N.generateSessionId(),this._sdpSessionVersion=0,this._dtlsRole=void 0,this._isClosed=!1};Object.defineProperty(n.prototype,"localDescription",{configurable:!0,get:function(){return this._localDescription}}),Object.defineProperty(n.prototype,"remoteDescription",{configurable:!0,get:function(){return this._remoteDescription}}),n.prototype.onicecandidate=null,n.prototype.onaddstream=null,n.prototype.ontrack=null,n.prototype.onremovestream=null,n.prototype.onsignalingstatechange=null,n.prototype.oniceconnectionstatechange=null,n.prototype.onconnectionstatechange=null,n.prototype.onicegatheringstatechange=null,n.prototype.onnegotiationneeded=null,n.prototype.ondatachannel=null,n.prototype._dispatchEvent=function(e,t){this._isClosed||(this.dispatchEvent(t),"function"==typeof this["on"+e]&&this["on"+e](t))},n.prototype._emitGatheringStateChange=function(){var e=new Event("icegatheringstatechange");this._dispatchEvent("icegatheringstatechange",e)},n.prototype.getConfiguration=function(){return this._config},n.prototype.getLocalStreams=function(){return this.localStreams},n.prototype.getRemoteStreams=function(){return this.remoteStreams},n.prototype._createTransceiver=function(e,t){var r=0<this.transceivers.length,n={track:null,iceGatherer:null,iceTransport:null,dtlsTransport:null,localCapabilities:null,remoteCapabilities:null,rtpSender:null,rtpReceiver:null,kind:e,mid:null,sendEncodingParameters:null,recvEncodingParameters:null,stream:null,associatedRemoteMediaStreams:[],wantReceive:!0};if(this.usingBundle&&r)n.iceTransport=this.transceivers[0].iceTransport,n.dtlsTransport=this.transceivers[0].dtlsTransport;else{var i=this._createIceAndDtlsTransports();n.iceTransport=i.iceTransport,n.dtlsTransport=i.dtlsTransport}return t||this.transceivers.push(n),n},n.prototype.addTrack=function(t,e){if(this._isClosed)throw m("InvalidStateError","Attempted to call addTrack on a closed peerconnection.");var r;if(this.transceivers.find(function(e){return e.track===t}))throw m("InvalidAccessError","Track already exists.");for(var n=0;n<this.transceivers.length;n++)this.transceivers[n].track||this.transceivers[n].kind!==t.kind||(r=this.transceivers[n]);return r||(r=this._createTransceiver(t.kind)),this._maybeFireNegotiationNeeded(),-1===this.localStreams.indexOf(e)&&this.localStreams.push(e),r.track=t,r.stream=e,r.rtpSender=new I.RTCRtpSender(t,r.dtlsTransport),r.rtpSender},n.prototype.addStream=function(t){var r=this;if(15025<=L)t.getTracks().forEach(function(e){r.addTrack(e,t)});else{var n=t.clone();t.getTracks().forEach(function(e,t){var r=n.getTracks()[t];e.addEventListener("enabled",function(e){r.enabled=e.enabled})}),n.getTracks().forEach(function(e){r.addTrack(e,n)})}},n.prototype.removeTrack=function(t){if(this._isClosed)throw m("InvalidStateError","Attempted to call removeTrack on a closed peerconnection.");if(!(t instanceof I.RTCRtpSender))throw new TypeError("Argument 1 of RTCPeerConnection.removeTrack does not implement interface RTCRtpSender.");var e=this.transceivers.find(function(e){return e.rtpSender===t});if(!e)throw m("InvalidAccessError","Sender was not created by this connection.");var r=e.stream;e.rtpSender.stop(),e.rtpSender=null,e.track=null,e.stream=null,-1===this.transceivers.map(function(e){return e.stream}).indexOf(r)&&-1<this.localStreams.indexOf(r)&&this.localStreams.splice(this.localStreams.indexOf(r),1),this._maybeFireNegotiationNeeded()},n.prototype.removeStream=function(e){var r=this;e.getTracks().forEach(function(t){var e=r.getSenders().find(function(e){return e.track===t});e&&r.removeTrack(e)})},n.prototype.getSenders=function(){return this.transceivers.filter(function(e){return!!e.rtpSender}).map(function(e){return e.rtpSender})},n.prototype.getReceivers=function(){return this.transceivers.filter(function(e){return!!e.rtpReceiver}).map(function(e){return e.rtpReceiver})},n.prototype._createIceGatherer=function(r,e){var n=this;if(e&&0<r)return this.transceivers[0].iceGatherer;if(this._iceGatherers.length)return this._iceGatherers.shift();var i=new I.RTCIceGatherer({iceServers:this._config.iceServers,gatherPolicy:this._config.iceTransportPolicy});return Object.defineProperty(i,"state",{value:"new",writable:!0}),this.transceivers[r].bufferedCandidateEvents=[],this.transceivers[r].bufferCandidates=function(e){var t=!e.candidate||0===Object.keys(e.candidate).length;i.state=t?"completed":"gathering",null!==n.transceivers[r].bufferedCandidateEvents&&n.transceivers[r].bufferedCandidateEvents.push(e)},i.addEventListener("localcandidate",this.transceivers[r].bufferCandidates),i},n.prototype._gather=function(s,c){var d=this,p=this.transceivers[c].iceGatherer;if(!p.onlocalcandidate){var e=this.transceivers[c].bufferedCandidateEvents;this.transceivers[c].bufferedCandidateEvents=null,p.removeEventListener("localcandidate",this.transceivers[c].bufferCandidates),p.onlocalcandidate=function(e){if(!(d.usingBundle&&0<c)){var t=new Event("icecandidate");t.candidate={sdpMid:s,sdpMLineIndex:c};var r=e.candidate,n=!r||0===Object.keys(r).length;if(n)"new"!==p.state&&"gathering"!==p.state||(p.state="completed");else{"new"===p.state&&(p.state="gathering"),r.component=1,r.ufrag=p.getLocalParameters().usernameFragment;var i=N.writeCandidate(r);t.candidate=Object.assign(t.candidate,N.parseCandidate(i)),t.candidate.candidate=i,t.candidate.toJSON=function(){return{candidate:t.candidate.candidate,sdpMid:t.candidate.sdpMid,sdpMLineIndex:t.candidate.sdpMLineIndex,usernameFragment:t.candidate.usernameFragment}}}var a=N.getMediaSections(d._localDescription.sdp);a[t.candidate.sdpMLineIndex]+=n?"a=end-of-candidates\r\n":"a="+t.candidate.candidate+"\r\n",d._localDescription.sdp=N.getDescription(d._localDescription.sdp)+a.join("");var o=d.transceivers.every(function(e){return e.iceGatherer&&"completed"===e.iceGatherer.state});"gathering"!==d.iceGatheringState&&(d.iceGatheringState="gathering",d._emitGatheringStateChange()),n||d._dispatchEvent("icecandidate",t),o&&(d._dispatchEvent("icecandidate",new Event("icecandidate")),d.iceGatheringState="complete",d._emitGatheringStateChange())}},I.setTimeout(function(){e.forEach(function(e){p.onlocalcandidate(e)})},0)}},n.prototype._createIceAndDtlsTransports=function(){var e=this,t=new I.RTCIceTransport(null);t.onicestatechange=function(){e._updateIceConnectionState(),e._updateConnectionState()};var r=new I.RTCDtlsTransport(t);return r.ondtlsstatechange=function(){e._updateConnectionState()},r.onerror=function(){Object.defineProperty(r,"state",{value:"failed",writable:!0}),e._updateConnectionState()},{iceTransport:t,dtlsTransport:r}},n.prototype._disposeIceAndDtlsTransports=function(e){var t=this.transceivers[e].iceGatherer;t&&(delete t.onlocalcandidate,delete this.transceivers[e].iceGatherer);var r=this.transceivers[e].iceTransport;r&&(delete r.onicestatechange,delete this.transceivers[e].iceTransport);var n=this.transceivers[e].dtlsTransport;n&&(delete n.ondtlsstatechange,delete n.onerror,delete this.transceivers[e].dtlsTransport)},n.prototype._transceive=function(e,t,r){var n=A(e.localCapabilities,e.remoteCapabilities);t&&e.rtpSender&&(n.encodings=e.sendEncodingParameters,n.rtcp={cname:N.localCName,compound:e.rtcpParameters.compound},e.recvEncodingParameters.length&&(n.rtcp.ssrc=e.recvEncodingParameters[0].ssrc),e.rtpSender.send(n)),r&&e.rtpReceiver&&0<n.codecs.length&&("video"===e.kind&&e.recvEncodingParameters&&L<15019&&e.recvEncodingParameters.forEach(function(e){delete e.rtx}),e.recvEncodingParameters.length?n.encodings=e.recvEncodingParameters:n.encodings=[{}],n.rtcp={compound:e.rtcpParameters.compound},e.rtcpParameters.cname&&(n.rtcp.cname=e.rtcpParameters.cname),e.sendEncodingParameters.length&&(n.rtcp.ssrc=e.sendEncodingParameters[0].ssrc),e.rtpReceiver.receive(n))},n.prototype.setLocalDescription=function(e){var t,u,f=this;if(-1===["offer","answer"].indexOf(e.type))return Promise.reject(m("TypeError",'Unsupported type "'+e.type+'"'));if(!a("setLocalDescription",e.type,f.signalingState)||f._isClosed)return Promise.reject(m("InvalidStateError","Can not set local "+e.type+" in state "+f.signalingState));if("offer"===e.type)t=N.splitSections(e.sdp),u=t.shift(),t.forEach(function(e,t){var r=N.parseRtpParameters(e);f.transceivers[t].localCapabilities=r}),f.transceivers.forEach(function(e,t){f._gather(e.mid,t)});else if("answer"===e.type){t=N.splitSections(f._remoteDescription.sdp),u=t.shift();var l=0<N.matchPrefix(u,"a=ice-lite").length;t.forEach(function(e,t){var r=f.transceivers[t],n=r.iceGatherer,i=r.iceTransport,a=r.dtlsTransport,o=r.localCapabilities,s=r.remoteCapabilities;if(!(N.isRejected(e)&&0===N.matchPrefix(e,"a=bundle-only").length)&&!r.rejected){var c=N.getIceParameters(e,u),d=N.getDtlsParameters(e,u);l&&(d.role="server"),f.usingBundle&&0!==t||(f._gather(r.mid,t),"new"===i.state&&i.start(n,c,l?"controlling":"controlled"),"new"===a.state&&a.start(d));var p=A(o,s);f._transceive(r,0<p.codecs.length,!1)}})}return f._localDescription={type:e.type,sdp:e.sdp},"offer"===e.type?f._updateSignalingState("have-local-offer"):f._updateSignalingState("stable"),Promise.resolve()},n.prototype.setRemoteDescription=function(k){var w=this;if(-1===["offer","answer"].indexOf(k.type))return Promise.reject(m("TypeError",'Unsupported type "'+k.type+'"'));if(!a("setRemoteDescription",k.type,w.signalingState)||w._isClosed)return Promise.reject(m("InvalidStateError","Can not set remote "+k.type+" in state "+w.signalingState));var _={};w.remoteStreams.forEach(function(e){_[e.id]=e});var x=[],e=N.splitSections(k.sdp),D=e.shift(),O=0<N.matchPrefix(D,"a=ice-lite").length,M=0<N.matchPrefix(D,"a=group:BUNDLE ").length;w.usingBundle=M;var t=N.matchPrefix(D,"a=ice-options:")[0];return w.canTrickleIceCandidates=!!t&&0<=t.substr(14).split(" ").indexOf("trickle"),e.forEach(function(e,t){var r=N.splitLines(e),n=N.getKind(e),i=N.isRejected(e)&&0===N.matchPrefix(e,"a=bundle-only").length,a=r[0].substr(2).split(" ")[2],o=N.getDirection(e,D),s=N.parseMsid(e),c=N.getMid(e)||N.generateIdentifier();if(i||"application"===n&&("DTLS/SCTP"===a||"UDP/DTLS/SCTP"===a))w.transceivers[t]={mid:c,kind:n,protocol:a,rejected:!0};else{var d,p,u,f,l,m,v,h,g;!i&&w.transceivers[t]&&w.transceivers[t].rejected&&(w.transceivers[t]=w._createTransceiver(n,!0));var y,C,T=N.parseRtpParameters(e);i||(y=N.getIceParameters(e,D),(C=N.getDtlsParameters(e,D)).role="client"),v=N.parseRtpEncodingParameters(e);var S=N.parseRtcpParameters(e),R=0<N.matchPrefix(e,"a=end-of-candidates",D).length,P=N.matchPrefix(e,"a=candidate:").map(function(e){return N.parseCandidate(e)}).filter(function(e){return 1===e.component});if(("offer"===k.type||"answer"===k.type)&&!i&&M&&0<t&&w.transceivers[t]&&(w._disposeIceAndDtlsTransports(t),w.transceivers[t].iceGatherer=w.transceivers[0].iceGatherer,w.transceivers[t].iceTransport=w.transceivers[0].iceTransport,w.transceivers[t].dtlsTransport=w.transceivers[0].dtlsTransport,w.transceivers[t].rtpSender&&w.transceivers[t].rtpSender.setTransport(w.transceivers[0].dtlsTransport),w.transceivers[t].rtpReceiver&&w.transceivers[t].rtpReceiver.setTransport(w.transceivers[0].dtlsTransport)),"offer"!==k.type||i){if("answer"===k.type&&!i){p=(d=w.transceivers[t]).iceGatherer,u=d.iceTransport,f=d.dtlsTransport,l=d.rtpReceiver,m=d.sendEncodingParameters,h=d.localCapabilities,w.transceivers[t].recvEncodingParameters=v,w.transceivers[t].remoteCapabilities=T,w.transceivers[t].rtcpParameters=S,P.length&&"new"===u.state&&(!O&&!R||M&&0!==t?P.forEach(function(e){U(d.iceTransport,e)}):u.setRemoteCandidates(P)),M&&0!==t||("new"===u.state&&u.start(p,y,"controlling"),"new"===f.state&&f.start(C)),!A(d.localCapabilities,d.remoteCapabilities).codecs.filter(function(e){return"rtx"===e.name.toLowerCase()}).length&&d.sendEncodingParameters[0].rtx&&delete d.sendEncodingParameters[0].rtx,w._transceive(d,"sendrecv"===o||"recvonly"===o,"sendrecv"===o||"sendonly"===o),!l||"sendrecv"!==o&&"sendonly"!==o?delete d.rtpReceiver:(g=l.track,s?(_[s.stream]||(_[s.stream]=new I.MediaStream),j(g,_[s.stream]),x.push([g,l,_[s.stream]])):(_.default||(_.default=new I.MediaStream),j(g,_.default),x.push([g,l,_.default])))}}else{(d=w.transceivers[t]||w._createTransceiver(n)).mid=c,d.iceGatherer||(d.iceGatherer=w._createIceGatherer(t,M)),P.length&&"new"===d.iceTransport.state&&(!R||M&&0!==t?P.forEach(function(e){U(d.iceTransport,e)}):d.iceTransport.setRemoteCandidates(P)),h=I.RTCRtpReceiver.getCapabilities(n),L<15019&&(h.codecs=h.codecs.filter(function(e){return"rtx"!==e.name})),m=d.sendEncodingParameters||[{ssrc:1001*(2*t+2)}];var E,b=!1;if("sendrecv"===o||"sendonly"===o){if(b=!d.rtpReceiver,l=d.rtpReceiver||new I.RTCRtpReceiver(d.dtlsTransport,n),b)g=l.track,s&&"-"===s.stream||(s?(_[s.stream]||(_[s.stream]=new I.MediaStream,Object.defineProperty(_[s.stream],"id",{get:function(){return s.stream}})),Object.defineProperty(g,"id",{get:function(){return s.track}}),E=_[s.stream]):(_.default||(_.default=new I.MediaStream),E=_.default)),E&&(j(g,E),d.associatedRemoteMediaStreams.push(E)),x.push([g,l,E])}else d.rtpReceiver&&d.rtpReceiver.track&&(d.associatedRemoteMediaStreams.forEach(function(e){var t,r,n=e.getTracks().find(function(e){return e.id===d.rtpReceiver.track.id});n&&(t=n,(r=e).removeTrack(t),r.dispatchEvent(new I.MediaStreamTrackEvent("removetrack",{track:t})))}),d.associatedRemoteMediaStreams=[]);d.localCapabilities=h,d.remoteCapabilities=T,d.rtpReceiver=l,d.rtcpParameters=S,d.sendEncodingParameters=m,d.recvEncodingParameters=v,w._transceive(w.transceivers[t],!1,b)}}}),void 0===w._dtlsRole&&(w._dtlsRole="offer"===k.type?"active":"passive"),w._remoteDescription={type:k.type,sdp:k.sdp},"offer"===k.type?w._updateSignalingState("have-remote-offer"):w._updateSignalingState("stable"),Object.keys(_).forEach(function(e){var n=_[e];if(n.getTracks().length){if(-1===w.remoteStreams.indexOf(n)){w.remoteStreams.push(n);var t=new Event("addstream");t.stream=n,I.setTimeout(function(){w._dispatchEvent("addstream",t)})}x.forEach(function(e){var t=e[0],r=e[1];n.id===e[2].id&&i(w,t,r,[n])})}}),x.forEach(function(e){e[2]||i(w,e[0],e[1],[])}),I.setTimeout(function(){w&&w.transceivers&&w.transceivers.forEach(function(e){e.iceTransport&&"new"===e.iceTransport.state&&0<e.iceTransport.getRemoteCandidates().length&&(console.warn("Timeout for addRemoteCandidate. Consider sending an end-of-candidates notification"),e.iceTransport.addRemoteCandidate({}))})},4e3),Promise.resolve()},n.prototype.close=function(){this.transceivers.forEach(function(e){e.iceTransport&&e.iceTransport.stop(),e.dtlsTransport&&e.dtlsTransport.stop(),e.rtpSender&&e.rtpSender.stop(),e.rtpReceiver&&e.rtpReceiver.stop()}),this._isClosed=!0,this._updateSignalingState("closed")},n.prototype._updateSignalingState=function(e){this.signalingState=e;var t=new Event("signalingstatechange");this._dispatchEvent("signalingstatechange",t)},n.prototype._maybeFireNegotiationNeeded=function(){var t=this;"stable"===this.signalingState&&!0!==this.needNegotiation&&(this.needNegotiation=!0,I.setTimeout(function(){if(t.needNegotiation){t.needNegotiation=!1;var e=new Event("negotiationneeded");t._dispatchEvent("negotiationneeded",e)}},0))},n.prototype._updateIceConnectionState=function(){var e,t={new:0,closed:0,checking:0,connected:0,completed:0,disconnected:0,failed:0};if(this.transceivers.forEach(function(e){t[e.iceTransport.state]++}),e="new",0<t.failed?e="failed":0<t.checking?e="checking":0<t.disconnected?e="disconnected":0<t.new?e="new":0<t.connected?e="connected":0<t.completed&&(e="completed"),e!==this.iceConnectionState){this.iceConnectionState=e;var r=new Event("iceconnectionstatechange");this._dispatchEvent("iceconnectionstatechange",r)}},n.prototype._updateConnectionState=function(){var e,t={new:0,closed:0,connecting:0,connected:0,completed:0,disconnected:0,failed:0};if(this.transceivers.forEach(function(e){t[e.iceTransport.state]++,t[e.dtlsTransport.state]++}),t.connected+=t.completed,e="new",0<t.failed?e="failed":0<t.connecting?e="connecting":0<t.disconnected?e="disconnected":0<t.new?e="new":0<t.connected&&(e="connected"),e!==this.connectionState){this.connectionState=e;var r=new Event("connectionstatechange");this._dispatchEvent("connectionstatechange",r)}},n.prototype.createOffer=function(){var s=this;if(s._isClosed)return Promise.reject(m("InvalidStateError","Can not call createOffer after close"));var t=s.transceivers.filter(function(e){return"audio"===e.kind}).length,r=s.transceivers.filter(function(e){return"video"===e.kind}).length,e=arguments[0];if(e){if(e.mandatory||e.optional)throw new TypeError("Legacy mandatory/optional constraints not supported.");void 0!==e.offerToReceiveAudio&&(t=!0===e.offerToReceiveAudio?1:!1===e.offerToReceiveAudio?0:e.offerToReceiveAudio),void 0!==e.offerToReceiveVideo&&(r=!0===e.offerToReceiveVideo?1:!1===e.offerToReceiveVideo?0:e.offerToReceiveVideo)}for(s.transceivers.forEach(function(e){"audio"===e.kind?--t<0&&(e.wantReceive=!1):"video"===e.kind&&--r<0&&(e.wantReceive=!1)});0<t||0<r;)0<t&&(s._createTransceiver("audio"),t--),0<r&&(s._createTransceiver("video"),r--);var n=N.writeSessionBoilerplate(s._sdpSessionId,s._sdpSessionVersion++);s.transceivers.forEach(function(e,t){var r=e.track,n=e.kind,i=e.mid||N.generateIdentifier();e.mid=i,e.iceGatherer||(e.iceGatherer=s._createIceGatherer(t,s.usingBundle));var a=I.RTCRtpSender.getCapabilities(n);L<15019&&(a.codecs=a.codecs.filter(function(e){return"rtx"!==e.name})),a.codecs.forEach(function(t){"H264"===t.name&&void 0===t.parameters["level-asymmetry-allowed"]&&(t.parameters["level-asymmetry-allowed"]="1"),e.remoteCapabilities&&e.remoteCapabilities.codecs&&e.remoteCapabilities.codecs.forEach(function(e){t.name.toLowerCase()===e.name.toLowerCase()&&t.clockRate===e.clockRate&&(t.preferredPayloadType=e.payloadType)})}),a.headerExtensions.forEach(function(t){(e.remoteCapabilities&&e.remoteCapabilities.headerExtensions||[]).forEach(function(e){t.uri===e.uri&&(t.id=e.id)})});var o=e.sendEncodingParameters||[{ssrc:1001*(2*t+1)}];r&&15019<=L&&"video"===n&&!o[0].rtx&&(o[0].rtx={ssrc:o[0].ssrc+1}),e.wantReceive&&(e.rtpReceiver=new I.RTCRtpReceiver(e.dtlsTransport,n)),e.localCapabilities=a,e.sendEncodingParameters=o}),"max-compat"!==s._config.bundlePolicy&&(n+="a=group:BUNDLE "+s.transceivers.map(function(e){return e.mid}).join(" ")+"\r\n"),n+="a=ice-options:trickle\r\n",s.transceivers.forEach(function(e,t){n+=c(e,e.localCapabilities,"offer",e.stream,s._dtlsRole),n+="a=rtcp-rsize\r\n",!e.iceGatherer||"new"===s.iceGatheringState||0!==t&&s.usingBundle||(e.iceGatherer.getLocalCandidates().forEach(function(e){e.component=1,n+="a="+N.writeCandidate(e)+"\r\n"}),"completed"===e.iceGatherer.state&&(n+="a=end-of-candidates\r\n"))});var i=new I.RTCSessionDescription({type:"offer",sdp:n});return Promise.resolve(i)},n.prototype.createAnswer=function(){var i=this;if(i._isClosed)return Promise.reject(m("InvalidStateError","Can not call createAnswer after close"));if("have-remote-offer"!==i.signalingState&&"have-local-pranswer"!==i.signalingState)return Promise.reject(m("InvalidStateError","Can not call createAnswer in signalingState "+i.signalingState));var a=N.writeSessionBoilerplate(i._sdpSessionId,i._sdpSessionVersion++);i.usingBundle&&(a+="a=group:BUNDLE "+i.transceivers.map(function(e){return e.mid}).join(" ")+"\r\n"),a+="a=ice-options:trickle\r\n";var o=N.getMediaSections(i._remoteDescription.sdp).length;i.transceivers.forEach(function(e,t){if(!(o<t+1)){if(e.rejected)return"application"===e.kind?"DTLS/SCTP"===e.protocol?a+="m=application 0 DTLS/SCTP 5000\r\n":a+="m=application 0 "+e.protocol+" webrtc-datachannel\r\n":"audio"===e.kind?a+="m=audio 0 UDP/TLS/RTP/SAVPF 0\r\na=rtpmap:0 PCMU/8000\r\n":"video"===e.kind&&(a+="m=video 0 UDP/TLS/RTP/SAVPF 120\r\na=rtpmap:120 VP8/90000\r\n"),void(a+="c=IN IP4 0.0.0.0\r\na=inactive\r\na=mid:"+e.mid+"\r\n");var r;if(e.stream)"audio"===e.kind?r=e.stream.getAudioTracks()[0]:"video"===e.kind&&(r=e.stream.getVideoTracks()[0]),r&&15019<=L&&"video"===e.kind&&!e.sendEncodingParameters[0].rtx&&(e.sendEncodingParameters[0].rtx={ssrc:e.sendEncodingParameters[0].ssrc+1});var n=A(e.localCapabilities,e.remoteCapabilities);!n.codecs.filter(function(e){return"rtx"===e.name.toLowerCase()}).length&&e.sendEncodingParameters[0].rtx&&delete e.sendEncodingParameters[0].rtx,a+=c(e,n,"answer",e.stream,i._dtlsRole),e.rtcpParameters&&e.rtcpParameters.reducedSize&&(a+="a=rtcp-rsize\r\n")}});var e=new I.RTCSessionDescription({type:"answer",sdp:a});return Promise.resolve(e)},n.prototype.addIceCandidate=function(c){var d,p=this;return c&&void 0===c.sdpMLineIndex&&!c.sdpMid?Promise.reject(new TypeError("sdpMLineIndex or sdpMid required")):new Promise(function(e,t){if(!p._remoteDescription)return t(m("InvalidStateError","Can not add ICE candidate without a remote description"));if(c&&""!==c.candidate){var r=c.sdpMLineIndex;if(c.sdpMid)for(var n=0;n<p.transceivers.length;n++)if(p.transceivers[n].mid===c.sdpMid){r=n;break}var i=p.transceivers[r];if(!i)return t(m("OperationError","Can not add ICE candidate"));if(i.rejected)return e();var a=0<Object.keys(c.candidate).length?N.parseCandidate(c.candidate):{};if("tcp"===a.protocol&&(0===a.port||9===a.port))return e();if(a.component&&1!==a.component)return e();if((0===r||0<r&&i.iceTransport!==p.transceivers[0].iceTransport)&&!U(i.iceTransport,a))return t(m("OperationError","Can not add ICE candidate"));var o=c.candidate.trim();0===o.indexOf("a=")&&(o=o.substr(2)),(d=N.getMediaSections(p._remoteDescription.sdp))[r]+="a="+(a.type?o:"end-of-candidates")+"\r\n",p._remoteDescription.sdp=N.getDescription(p._remoteDescription.sdp)+d.join("")}else for(var s=0;s<p.transceivers.length&&(p.transceivers[s].rejected||(p.transceivers[s].iceTransport.addRemoteCandidate({}),(d=N.getMediaSections(p._remoteDescription.sdp))[s]+="a=end-of-candidates\r\n",p._remoteDescription.sdp=N.getDescription(p._remoteDescription.sdp)+d.join(""),!p.usingBundle));s++);e()})},n.prototype.getStats=function(t){if(t&&t instanceof I.MediaStreamTrack){var r=null;if(this.transceivers.forEach(function(e){e.rtpSender&&e.rtpSender.track===t?r=e.rtpSender:e.rtpReceiver&&e.rtpReceiver.track===t&&(r=e.rtpReceiver)}),!r)throw m("InvalidAccessError","Invalid selector.");return r.getStats()}var n=[];return this.transceivers.forEach(function(t){["rtpSender","rtpReceiver","iceGatherer","iceTransport","dtlsTransport"].forEach(function(e){t[e]&&n.push(t[e].getStats())})}),Promise.all(n).then(function(e){var t=new Map;return e.forEach(function(e){e.forEach(function(e){t.set(e.id,e)})}),t})};["RTCRtpSender","RTCRtpReceiver","RTCIceGatherer","RTCIceTransport","RTCDtlsTransport"].forEach(function(e){var t=I[e];if(t&&t.prototype&&t.prototype.getStats){var r=t.prototype.getStats;t.prototype.getStats=function(){return r.apply(this).then(function(r){var n=new Map;return Object.keys(r).forEach(function(e){var t;r[e].type={inboundrtp:"inbound-rtp",outboundrtp:"outbound-rtp",candidatepair:"candidate-pair",localcandidate:"local-candidate",remotecandidate:"remote-candidate"}[(t=r[e]).type]||t.type,n.set(e,r[e])}),n})}}});var e=["createOffer","createAnswer"];return e.forEach(function(e){var r=n.prototype[e];n.prototype[e]=function(){var t=arguments;return"function"==typeof t[0]||"function"==typeof t[1]?r.apply(this,[arguments[2]]).then(function(e){"function"==typeof t[0]&&t[0].apply(null,[e])},function(e){"function"==typeof t[1]&&t[1].apply(null,[e])}):r.apply(this,arguments)}}),(e=["setLocalDescription","setRemoteDescription","addIceCandidate"]).forEach(function(e){var r=n.prototype[e];n.prototype[e]=function(){var t=arguments;return"function"==typeof t[1]||"function"==typeof t[2]?r.apply(this,arguments).then(function(){"function"==typeof t[1]&&t[1].apply(null)},function(e){"function"==typeof t[2]&&t[2].apply(null,[e])}):r.apply(this,arguments)}}),["getStats"].forEach(function(e){var t=n.prototype[e];n.prototype[e]=function(){var e=arguments;return"function"==typeof e[1]?t.apply(this,arguments).then(function(){"function"==typeof e[1]&&e[1].apply(null)}):t.apply(this,arguments)}}),n}},{sdp:2}],2:[function(e,t,r){"use strict";var p={generateIdentifier:function(){return Math.random().toString(36).substr(2,10)}};p.localCName=p.generateIdentifier(),p.splitLines=function(e){return e.trim().split("\n").map(function(e){return e.trim()})},p.splitSections=function(e){return e.split("\nm=").map(function(e,t){return(0<t?"m="+e:e).trim()+"\r\n"})},p.getDescription=function(e){var t=p.splitSections(e);return t&&t[0]},p.getMediaSections=function(e){var t=p.splitSections(e);return t.shift(),t},p.matchPrefix=function(e,t){return p.splitLines(e).filter(function(e){return 0===e.indexOf(t)})},p.parseCandidate=function(e){for(var t,r={foundation:(t=0===e.indexOf("a=candidate:")?e.substring(12).split(" "):e.substring(10).split(" "))[0],component:parseInt(t[1],10),protocol:t[2].toLowerCase(),priority:parseInt(t[3],10),ip:t[4],address:t[4],port:parseInt(t[5],10),type:t[7]},n=8;n<t.length;n+=2)switch(t[n]){case"raddr":r.relatedAddress=t[n+1];break;case"rport":r.relatedPort=parseInt(t[n+1],10);break;case"tcptype":r.tcpType=t[n+1];break;case"ufrag":r.ufrag=t[n+1],r.usernameFragment=t[n+1];break;default:r[t[n]]=t[n+1]}return r},p.writeCandidate=function(e){var t=[];t.push(e.foundation),t.push(e.component),t.push(e.protocol.toUpperCase()),t.push(e.priority),t.push(e.address||e.ip),t.push(e.port);var r=e.type;return t.push("typ"),t.push(r),"host"!==r&&e.relatedAddress&&e.relatedPort&&(t.push("raddr"),t.push(e.relatedAddress),t.push("rport"),t.push(e.relatedPort)),e.tcpType&&"tcp"===e.protocol.toLowerCase()&&(t.push("tcptype"),t.push(e.tcpType)),(e.usernameFragment||e.ufrag)&&(t.push("ufrag"),t.push(e.usernameFragment||e.ufrag)),"candidate:"+t.join(" ")},p.parseIceOptions=function(e){return e.substr(14).split(" ")},p.parseRtpMap=function(e){var t=e.substr(9).split(" "),r={payloadType:parseInt(t.shift(),10)};return t=t[0].split("/"),r.name=t[0],r.clockRate=parseInt(t[1],10),r.channels=3===t.length?parseInt(t[2],10):1,r.numChannels=r.channels,r},p.writeRtpMap=function(e){var t=e.payloadType;void 0!==e.preferredPayloadType&&(t=e.preferredPayloadType);var r=e.channels||e.numChannels||1;return"a=rtpmap:"+t+" "+e.name+"/"+e.clockRate+(1!==r?"/"+r:"")+"\r\n"},p.parseExtmap=function(e){var t=e.substr(9).split(" ");return{id:parseInt(t[0],10),direction:0<t[0].indexOf("/")?t[0].split("/")[1]:"sendrecv",uri:t[1]}},p.writeExtmap=function(e){return"a=extmap:"+(e.id||e.preferredId)+(e.direction&&"sendrecv"!==e.direction?"/"+e.direction:"")+" "+e.uri+"\r\n"},p.parseFmtp=function(e){for(var t,r={},n=e.substr(e.indexOf(" ")+1).split(";"),i=0;i<n.length;i++)r[(t=n[i].trim().split("="))[0].trim()]=t[1];return r},p.writeFmtp=function(t){var e="",r=t.payloadType;if(void 0!==t.preferredPayloadType&&(r=t.preferredPayloadType),t.parameters&&Object.keys(t.parameters).length){var n=[];Object.keys(t.parameters).forEach(function(e){t.parameters[e]?n.push(e+"="+t.parameters[e]):n.push(e)}),e+="a=fmtp:"+r+" "+n.join(";")+"\r\n"}return e},p.parseRtcpFb=function(e){var t=e.substr(e.indexOf(" ")+1).split(" ");return{type:t.shift(),parameter:t.join(" ")}},p.writeRtcpFb=function(e){var t="",r=e.payloadType;return void 0!==e.preferredPayloadType&&(r=e.preferredPayloadType),e.rtcpFeedback&&e.rtcpFeedback.length&&e.rtcpFeedback.forEach(function(e){t+="a=rtcp-fb:"+r+" "+e.type+(e.parameter&&e.parameter.length?" "+e.parameter:"")+"\r\n"}),t},p.parseSsrcMedia=function(e){var t=e.indexOf(" "),r={ssrc:parseInt(e.substr(7,t-7),10)},n=e.indexOf(":",t);return-1<n?(r.attribute=e.substr(t+1,n-t-1),r.value=e.substr(n+1)):r.attribute=e.substr(t+1),r},p.parseSsrcGroup=function(e){var t=e.substr(13).split(" ");return{semantics:t.shift(),ssrcs:t.map(function(e){return parseInt(e,10)})}},p.getMid=function(e){var t=p.matchPrefix(e,"a=mid:")[0];if(t)return t.substr(6)},p.parseFingerprint=function(e){var t=e.substr(14).split(" ");return{algorithm:t[0].toLowerCase(),value:t[1]}},p.getDtlsParameters=function(e,t){return{role:"auto",fingerprints:p.matchPrefix(e+t,"a=fingerprint:").map(p.parseFingerprint)}},p.writeDtlsParameters=function(e,t){var r="a=setup:"+t+"\r\n";return e.fingerprints.forEach(function(e){r+="a=fingerprint:"+e.algorithm+" "+e.value+"\r\n"}),r},p.getIceParameters=function(e,t){var r=p.splitLines(e);return{usernameFragment:(r=r.concat(p.splitLines(t))).filter(function(e){return 0===e.indexOf("a=ice-ufrag:")})[0].substr(12),password:r.filter(function(e){return 0===e.indexOf("a=ice-pwd:")})[0].substr(10)}},p.writeIceParameters=function(e){return"a=ice-ufrag:"+e.usernameFragment+"\r\na=ice-pwd:"+e.password+"\r\n"},p.parseRtpParameters=function(e){for(var t={codecs:[],headerExtensions:[],fecMechanisms:[],rtcp:[]},r=p.splitLines(e)[0].split(" "),n=3;n<r.length;n++){var i=r[n],a=p.matchPrefix(e,"a=rtpmap:"+i+" ")[0];if(a){var o=p.parseRtpMap(a),s=p.matchPrefix(e,"a=fmtp:"+i+" ");switch(o.parameters=s.length?p.parseFmtp(s[0]):{},o.rtcpFeedback=p.matchPrefix(e,"a=rtcp-fb:"+i+" ").map(p.parseRtcpFb),t.codecs.push(o),o.name.toUpperCase()){case"RED":case"ULPFEC":t.fecMechanisms.push(o.name.toUpperCase())}}}return p.matchPrefix(e,"a=extmap:").forEach(function(e){t.headerExtensions.push(p.parseExtmap(e))}),t},p.writeRtpDescription=function(e,t){var r="";r+="m="+e+" ",r+=0<t.codecs.length?"9":"0",r+=" UDP/TLS/RTP/SAVPF ",r+=t.codecs.map(function(e){return void 0!==e.preferredPayloadType?e.preferredPayloadType:e.payloadType}).join(" ")+"\r\n",r+="c=IN IP4 0.0.0.0\r\n",r+="a=rtcp:9 IN IP4 0.0.0.0\r\n",t.codecs.forEach(function(e){r+=p.writeRtpMap(e),r+=p.writeFmtp(e),r+=p.writeRtcpFb(e)});var n=0;return t.codecs.forEach(function(e){e.maxptime>n&&(n=e.maxptime)}),0<n&&(r+="a=maxptime:"+n+"\r\n"),r+="a=rtcp-mux\r\n",t.headerExtensions&&t.headerExtensions.forEach(function(e){r+=p.writeExtmap(e)}),r},p.parseRtpEncodingParameters=function(e){var r,n=[],t=p.parseRtpParameters(e),i=-1!==t.fecMechanisms.indexOf("RED"),a=-1!==t.fecMechanisms.indexOf("ULPFEC"),o=p.matchPrefix(e,"a=ssrc:").map(function(e){return p.parseSsrcMedia(e)}).filter(function(e){return"cname"===e.attribute}),s=0<o.length&&o[0].ssrc,c=p.matchPrefix(e,"a=ssrc-group:FID").map(function(e){return e.substr(17).split(" ").map(function(e){return parseInt(e,10)})});0<c.length&&1<c[0].length&&c[0][0]===s&&(r=c[0][1]),t.codecs.forEach(function(e){if("RTX"===e.name.toUpperCase()&&e.parameters.apt){var t={ssrc:s,codecPayloadType:parseInt(e.parameters.apt,10)};s&&r&&(t.rtx={ssrc:r}),n.push(t),i&&((t=JSON.parse(JSON.stringify(t))).fec={ssrc:s,mechanism:a?"red+ulpfec":"red"},n.push(t))}}),0===n.length&&s&&n.push({ssrc:s});var d=p.matchPrefix(e,"b=");return d.length&&(d=0===d[0].indexOf("b=TIAS:")?parseInt(d[0].substr(7),10):0===d[0].indexOf("b=AS:")?1e3*parseInt(d[0].substr(5),10)*.95-16e3:void 0,n.forEach(function(e){e.maxBitrate=d})),n},p.parseRtcpParameters=function(e){var t={},r=p.matchPrefix(e,"a=ssrc:").map(function(e){return p.parseSsrcMedia(e)}).filter(function(e){return"cname"===e.attribute})[0];r&&(t.cname=r.value,t.ssrc=r.ssrc);var n=p.matchPrefix(e,"a=rtcp-rsize");t.reducedSize=0<n.length,t.compound=0===n.length;var i=p.matchPrefix(e,"a=rtcp-mux");return t.mux=0<i.length,t},p.parseMsid=function(e){var t,r=p.matchPrefix(e,"a=msid:");if(1===r.length)return{stream:(t=r[0].substr(7).split(" "))[0],track:t[1]};var n=p.matchPrefix(e,"a=ssrc:").map(function(e){return p.parseSsrcMedia(e)}).filter(function(e){return"msid"===e.attribute});return 0<n.length?{stream:(t=n[0].value.split(" "))[0],track:t[1]}:void 0},p.generateSessionId=function(){return Math.random().toString().substr(2,21)},p.writeSessionBoilerplate=function(e,t,r){var n=void 0!==t?t:2;return"v=0\r\no="+(r||"thisisadapterortc")+" "+(e||p.generateSessionId())+" "+n+" IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\n"},p.writeMediaSection=function(e,t,r,n){var i=p.writeRtpDescription(e.kind,t);if(i+=p.writeIceParameters(e.iceGatherer.getLocalParameters()),i+=p.writeDtlsParameters(e.dtlsTransport.getLocalParameters(),"offer"===r?"actpass":"active"),i+="a=mid:"+e.mid+"\r\n",e.direction?i+="a="+e.direction+"\r\n":e.rtpSender&&e.rtpReceiver?i+="a=sendrecv\r\n":e.rtpSender?i+="a=sendonly\r\n":e.rtpReceiver?i+="a=recvonly\r\n":i+="a=inactive\r\n",e.rtpSender){var a="msid:"+n.id+" "+e.rtpSender.track.id+"\r\n";i+="a="+a,i+="a=ssrc:"+e.sendEncodingParameters[0].ssrc+" "+a,e.sendEncodingParameters[0].rtx&&(i+="a=ssrc:"+e.sendEncodingParameters[0].rtx.ssrc+" "+a,i+="a=ssrc-group:FID "+e.sendEncodingParameters[0].ssrc+" "+e.sendEncodingParameters[0].rtx.ssrc+"\r\n")}return i+="a=ssrc:"+e.sendEncodingParameters[0].ssrc+" cname:"+p.localCName+"\r\n",e.rtpSender&&e.sendEncodingParameters[0].rtx&&(i+="a=ssrc:"+e.sendEncodingParameters[0].rtx.ssrc+" cname:"+p.localCName+"\r\n"),i},p.getDirection=function(e,t){for(var r=p.splitLines(e),n=0;n<r.length;n++)switch(r[n]){case"a=sendrecv":case"a=sendonly":case"a=recvonly":case"a=inactive":return r[n].substr(2)}return t?p.getDirection(t):"sendrecv"},p.getKind=function(e){return p.splitLines(e)[0].split(" ")[0].substr(2)},p.isRejected=function(e){return"0"===e.split(" ",2)[1]},p.parseMLine=function(e){var t=p.splitLines(e)[0].substr(2).split(" ");return{kind:t[0],port:parseInt(t[1],10),protocol:t[2],fmt:t.slice(3).join(" ")}},p.parseOLine=function(e){var t=p.matchPrefix(e,"o=")[0].substr(2).split(" ");return{username:t[0],sessionId:t[1],sessionVersion:parseInt(t[2],10),netType:t[3],addressType:t[4],address:t[5]}},p.isValidSDP=function(e){if("string"!=typeof e||0===e.length)return!1;for(var t=p.splitLines(e),r=0;r<t.length;r++)if(t[r].length<2||"="!==t[r].charAt(1))return!1;return!0},"object"==typeof t&&(t.exports=p)},{}],3:[function(r,n,e){(function(e){"use strict";var t=r("./adapter_factory.js");n.exports=t({window:e.window})}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{"./adapter_factory.js":4}],4:[function(l,e,t){"use strict";var m=l("./utils");e.exports=function(e,t){var r=e&&e.window,n={shimChrome:!0,shimFirefox:!0,shimEdge:!0,shimSafari:!0};for(var i in t)hasOwnProperty.call(t,i)&&(n[i]=t[i]);var a=m.log,o=m.detectBrowser(r),s=l("./chrome/chrome_shim")||null,c=l("./edge/edge_shim")||null,d=l("./firefox/firefox_shim")||null,p=l("./safari/safari_shim")||null,u=l("./common_shim")||null,f={browserDetails:o,commonShim:u,extractVersion:m.extractVersion,disableLog:m.disableLog,disableWarnings:m.disableWarnings};switch(o.browser){case"chrome":if(!s||!s.shimPeerConnection||!n.shimChrome)return a("Chrome shim is not included in this adapter release."),f;a("adapter.js shimming chrome."),f.browserShim=s,u.shimCreateObjectURL(r),s.shimGetUserMedia(r),s.shimMediaStream(r),s.shimSourceObject(r),s.shimPeerConnection(r),s.shimOnTrack(r),s.shimAddTrackRemoveTrack(r),s.shimGetSendersWithDtmf(r),s.shimSenderReceiverGetStats(r),s.fixNegotiationNeeded(r),u.shimRTCIceCandidate(r),u.shimMaxMessageSize(r),u.shimSendThrowTypeError(r);break;case"firefox":if(!d||!d.shimPeerConnection||!n.shimFirefox)return a("Firefox shim is not included in this adapter release."),f;a("adapter.js shimming firefox."),f.browserShim=d,u.shimCreateObjectURL(r),d.shimGetUserMedia(r),d.shimSourceObject(r),d.shimPeerConnection(r),d.shimOnTrack(r),d.shimRemoveStream(r),d.shimSenderGetStats(r),d.shimReceiverGetStats(r),d.shimRTCDataChannel(r),u.shimRTCIceCandidate(r),u.shimMaxMessageSize(r),u.shimSendThrowTypeError(r);break;case"edge":if(!c||!c.shimPeerConnection||!n.shimEdge)return a("MS edge shim is not included in this adapter release."),f;a("adapter.js shimming edge."),f.browserShim=c,u.shimCreateObjectURL(r),c.shimGetUserMedia(r),c.shimPeerConnection(r),c.shimReplaceTrack(r),u.shimMaxMessageSize(r),u.shimSendThrowTypeError(r);break;case"safari":if(!p||!n.shimSafari)return a("Safari shim is not included in this adapter release."),f;a("adapter.js shimming safari."),f.browserShim=p,u.shimCreateObjectURL(r),p.shimRTCIceServerUrls(r),p.shimCreateOfferLegacy(r),p.shimCallbacksAPI(r),p.shimLocalStreamsAPI(r),p.shimRemoteStreamsAPI(r),p.shimTrackEventTransceiver(r),p.shimGetUserMedia(r),u.shimRTCIceCandidate(r),u.shimMaxMessageSize(r),u.shimSendThrowTypeError(r);break;default:a("Unsupported browser!")}return f}},{"./chrome/chrome_shim":5,"./common_shim":7,"./edge/edge_shim":8,"./firefox/firefox_shim":11,"./safari/safari_shim":13,"./utils":14}],5:[function(e,t,r){"use strict";var c=e("../utils.js"),n=c.log;function i(r,t,e){var n=e?"outbound-rtp":"inbound-rtp",i=new Map;if(null===t)return i;var a=[];return r.forEach(function(e){"track"===e.type&&e.trackIdentifier===t.id&&a.push(e)}),a.forEach(function(t){r.forEach(function(e){e.type===n&&e.trackId===t.id&&function t(r,n,i){n&&!i.has(n.id)&&(i.set(n.id,n),Object.keys(n).forEach(function(e){e.endsWith("Id")?t(r,r.get(n[e]),i):e.endsWith("Ids")&&n[e].forEach(function(e){t(r,r.get(e),i)})}))}(r,e,i)})}),i}t.exports={shimGetUserMedia:e("./getusermedia"),shimMediaStream:function(e){e.MediaStream=e.MediaStream||e.webkitMediaStream},shimOnTrack:function(a){if("object"!=typeof a||!a.RTCPeerConnection||"ontrack"in a.RTCPeerConnection.prototype)c.wrapPeerConnectionEvent(a,"track",function(e){return e.transceiver||Object.defineProperty(e,"transceiver",{value:{receiver:e.receiver}}),e});else{Object.defineProperty(a.RTCPeerConnection.prototype,"ontrack",{get:function(){return this._ontrack},set:function(e){this._ontrack&&this.removeEventListener("track",this._ontrack),this.addEventListener("track",this._ontrack=e)},enumerable:!0,configurable:!0});var e=a.RTCPeerConnection.prototype.setRemoteDescription;a.RTCPeerConnection.prototype.setRemoteDescription=function(){var i=this;return i._ontrackpoly||(i._ontrackpoly=function(n){n.stream.addEventListener("addtrack",function(t){var e;e=a.RTCPeerConnection.prototype.getReceivers?i.getReceivers().find(function(e){return e.track&&e.track.id===t.track.id}):{track:t.track};var r=new Event("track");r.track=t.track,r.receiver=e,r.transceiver={receiver:e},r.streams=[n.stream],i.dispatchEvent(r)}),n.stream.getTracks().forEach(function(t){var e;e=a.RTCPeerConnection.prototype.getReceivers?i.getReceivers().find(function(e){return e.track&&e.track.id===t.id}):{track:t};var r=new Event("track");r.track=t,r.receiver=e,r.transceiver={receiver:e},r.streams=[n.stream],i.dispatchEvent(r)})},i.addEventListener("addstream",i._ontrackpoly)),e.apply(i,arguments)}}},shimGetSendersWithDtmf:function(e){if("object"==typeof e&&e.RTCPeerConnection&&!("getSenders"in e.RTCPeerConnection.prototype)&&"createDTMFSender"in e.RTCPeerConnection.prototype){var n=function(e,t){return{track:t,get dtmf(){return void 0===this._dtmf&&("audio"===t.kind?this._dtmf=e.createDTMFSender(t):this._dtmf=null),this._dtmf},_pc:e}};if(!e.RTCPeerConnection.prototype.getSenders){e.RTCPeerConnection.prototype.getSenders=function(){return this._senders=this._senders||[],this._senders.slice()};var i=e.RTCPeerConnection.prototype.addTrack;e.RTCPeerConnection.prototype.addTrack=function(e,t){var r=i.apply(this,arguments);return r||(r=n(this,e),this._senders.push(r)),r};var r=e.RTCPeerConnection.prototype.removeTrack;e.RTCPeerConnection.prototype.removeTrack=function(e){r.apply(this,arguments);var t=this._senders.indexOf(e);-1!==t&&this._senders.splice(t,1)}}var a=e.RTCPeerConnection.prototype.addStream;e.RTCPeerConnection.prototype.addStream=function(e){var t=this;t._senders=t._senders||[],a.apply(t,[e]),e.getTracks().forEach(function(e){t._senders.push(n(t,e))})};var t=e.RTCPeerConnection.prototype.removeStream;e.RTCPeerConnection.prototype.removeStream=function(e){var r=this;r._senders=r._senders||[],t.apply(r,[e]),e.getTracks().forEach(function(t){var e=r._senders.find(function(e){return e.track===t});e&&r._senders.splice(r._senders.indexOf(e),1)})}}else if("object"==typeof e&&e.RTCPeerConnection&&"getSenders"in e.RTCPeerConnection.prototype&&"createDTMFSender"in e.RTCPeerConnection.prototype&&e.RTCRtpSender&&!("dtmf"in e.RTCRtpSender.prototype)){var o=e.RTCPeerConnection.prototype.getSenders;e.RTCPeerConnection.prototype.getSenders=function(){var t=this,e=o.apply(t,[]);return e.forEach(function(e){e._pc=t}),e},Object.defineProperty(e.RTCRtpSender.prototype,"dtmf",{get:function(){return void 0===this._dtmf&&("audio"===this.track.kind?this._dtmf=this._pc.createDTMFSender(this.track):this._dtmf=null),this._dtmf}})}},shimSenderReceiverGetStats:function(e){if("object"==typeof e&&e.RTCPeerConnection&&e.RTCRtpSender&&e.RTCRtpReceiver){if(!("getStats"in e.RTCRtpSender.prototype)){var r=e.RTCPeerConnection.prototype.getSenders;r&&(e.RTCPeerConnection.prototype.getSenders=function(){var t=this,e=r.apply(t,[]);return e.forEach(function(e){e._pc=t}),e});var t=e.RTCPeerConnection.prototype.addTrack;t&&(e.RTCPeerConnection.prototype.addTrack=function(){var e=t.apply(this,arguments);return e._pc=this,e}),e.RTCRtpSender.prototype.getStats=function(){var t=this;return this._pc.getStats().then(function(e){return i(e,t.track,!0)})}}if(!("getStats"in e.RTCRtpReceiver.prototype)){var n=e.RTCPeerConnection.prototype.getReceivers;n&&(e.RTCPeerConnection.prototype.getReceivers=function(){var t=this,e=n.apply(t,[]);return e.forEach(function(e){e._pc=t}),e}),c.wrapPeerConnectionEvent(e,"track",function(e){return e.receiver._pc=e.srcElement,e}),e.RTCRtpReceiver.prototype.getStats=function(){var t=this;return this._pc.getStats().then(function(e){return i(e,t.track,!1)})}}if("getStats"in e.RTCRtpSender.prototype&&"getStats"in e.RTCRtpReceiver.prototype){var a=e.RTCPeerConnection.prototype.getStats;e.RTCPeerConnection.prototype.getStats=function(){if(0<arguments.length&&arguments[0]instanceof e.MediaStreamTrack){var t,r,n,i=arguments[0];return this.getSenders().forEach(function(e){e.track===i&&(t?n=!0:t=e)}),this.getReceivers().forEach(function(e){return e.track===i&&(r?n=!0:r=e),e.track===i}),n||t&&r?Promise.reject(new DOMException("There are more than one sender or receiver for the track.","InvalidAccessError")):t?t.getStats():r?r.getStats():Promise.reject(new DOMException("There is no sender or receiver for the track.","InvalidAccessError"))}return a.apply(this,arguments)}}}},shimSourceObject:function(e){var r=e&&e.URL;"object"==typeof e&&(!e.HTMLMediaElement||"srcObject"in e.HTMLMediaElement.prototype||Object.defineProperty(e.HTMLMediaElement.prototype,"srcObject",{get:function(){return this._srcObject},set:function(e){var t=this;this._srcObject=e,this.src&&r.revokeObjectURL(this.src),e?(this.src=r.createObjectURL(e),e.addEventListener("addtrack",function(){t.src&&r.revokeObjectURL(t.src),t.src=r.createObjectURL(e)}),e.addEventListener("removetrack",function(){t.src&&r.revokeObjectURL(t.src),t.src=r.createObjectURL(e)})):this.src=""}}))},shimAddTrackRemoveTrackWithNative:function(e){e.RTCPeerConnection.prototype.getLocalStreams=function(){var t=this;return this._shimmedLocalStreams=this._shimmedLocalStreams||{},Object.keys(this._shimmedLocalStreams).map(function(e){return t._shimmedLocalStreams[e][0]})};var n=e.RTCPeerConnection.prototype.addTrack;e.RTCPeerConnection.prototype.addTrack=function(e,t){if(!t)return n.apply(this,arguments);this._shimmedLocalStreams=this._shimmedLocalStreams||{};var r=n.apply(this,arguments);return this._shimmedLocalStreams[t.id]?-1===this._shimmedLocalStreams[t.id].indexOf(r)&&this._shimmedLocalStreams[t.id].push(r):this._shimmedLocalStreams[t.id]=[t,r],r};var i=e.RTCPeerConnection.prototype.addStream;e.RTCPeerConnection.prototype.addStream=function(e){var r=this;this._shimmedLocalStreams=this._shimmedLocalStreams||{},e.getTracks().forEach(function(t){if(r.getSenders().find(function(e){return e.track===t}))throw new DOMException("Track already exists.","InvalidAccessError")});var t=r.getSenders();i.apply(this,arguments);var n=r.getSenders().filter(function(e){return-1===t.indexOf(e)});this._shimmedLocalStreams[e.id]=[e].concat(n)};var t=e.RTCPeerConnection.prototype.removeStream;e.RTCPeerConnection.prototype.removeStream=function(e){return this._shimmedLocalStreams=this._shimmedLocalStreams||{},delete this._shimmedLocalStreams[e.id],t.apply(this,arguments)};var a=e.RTCPeerConnection.prototype.removeTrack;e.RTCPeerConnection.prototype.removeTrack=function(r){var n=this;return this._shimmedLocalStreams=this._shimmedLocalStreams||{},r&&Object.keys(this._shimmedLocalStreams).forEach(function(e){var t=n._shimmedLocalStreams[e].indexOf(r);-1!==t&&n._shimmedLocalStreams[e].splice(t,1),1===n._shimmedLocalStreams[e].length&&delete n._shimmedLocalStreams[e]}),a.apply(this,arguments)}},shimAddTrackRemoveTrack:function(o){var e=c.detectBrowser(o);if(o.RTCPeerConnection.prototype.addTrack&&65<=e.version)return this.shimAddTrackRemoveTrackWithNative(o);var r=o.RTCPeerConnection.prototype.getLocalStreams;o.RTCPeerConnection.prototype.getLocalStreams=function(){var t=this,e=r.apply(this);return t._reverseStreams=t._reverseStreams||{},e.map(function(e){return t._reverseStreams[e.id]})};var n=o.RTCPeerConnection.prototype.addStream;o.RTCPeerConnection.prototype.addStream=function(e){var r=this;if(r._streams=r._streams||{},r._reverseStreams=r._reverseStreams||{},e.getTracks().forEach(function(t){if(r.getSenders().find(function(e){return e.track===t}))throw new DOMException("Track already exists.","InvalidAccessError")}),!r._reverseStreams[e.id]){var t=new o.MediaStream(e.getTracks());r._streams[e.id]=t,r._reverseStreams[t.id]=e,e=t}n.apply(r,[e])};var i=o.RTCPeerConnection.prototype.removeStream;function a(n,e){var i=e.sdp;return Object.keys(n._reverseStreams||[]).forEach(function(e){var t=n._reverseStreams[e],r=n._streams[t.id];i=i.replace(new RegExp(r.id,"g"),t.id)}),new RTCSessionDescription({type:e.type,sdp:i})}o.RTCPeerConnection.prototype.removeStream=function(e){var t=this;t._streams=t._streams||{},t._reverseStreams=t._reverseStreams||{},i.apply(t,[t._streams[e.id]||e]),delete t._reverseStreams[t._streams[e.id]?t._streams[e.id].id:e.id],delete t._streams[e.id]},o.RTCPeerConnection.prototype.addTrack=function(t,e){var r=this;if("closed"===r.signalingState)throw new DOMException("The RTCPeerConnection's signalingState is 'closed'.","InvalidStateError");var n=[].slice.call(arguments,1);if(1!==n.length||!n[0].getTracks().find(function(e){return e===t}))throw new DOMException("The adapter.js addTrack polyfill only supports a single  stream which is associated with the specified track.","NotSupportedError");if(r.getSenders().find(function(e){return e.track===t}))throw new DOMException("Track already exists.","InvalidAccessError");r._streams=r._streams||{},r._reverseStreams=r._reverseStreams||{};var i=r._streams[e.id];if(i)i.addTrack(t),Promise.resolve().then(function(){r.dispatchEvent(new Event("negotiationneeded"))});else{var a=new o.MediaStream([t]);r._streams[e.id]=a,r._reverseStreams[a.id]=e,r.addStream(a)}return r.getSenders().find(function(e){return e.track===t})},["createOffer","createAnswer"].forEach(function(e){var t=o.RTCPeerConnection.prototype[e];o.RTCPeerConnection.prototype[e]=function(){var r=this,n=arguments;return arguments.length&&"function"==typeof arguments[0]?t.apply(r,[function(e){var t=a(r,e);n[0].apply(null,[t])},function(e){n[1]&&n[1].apply(null,e)},arguments[2]]):t.apply(r,arguments).then(function(e){return a(r,e)})}});var t=o.RTCPeerConnection.prototype.setLocalDescription;o.RTCPeerConnection.prototype.setLocalDescription=function(){var n,e,i;return arguments.length&&arguments[0].type&&(arguments[0]=(n=this,e=arguments[0],i=e.sdp,Object.keys(n._reverseStreams||[]).forEach(function(e){var t=n._reverseStreams[e],r=n._streams[t.id];i=i.replace(new RegExp(t.id,"g"),r.id)}),new RTCSessionDescription({type:e.type,sdp:i}))),t.apply(this,arguments)};var s=Object.getOwnPropertyDescriptor(o.RTCPeerConnection.prototype,"localDescription");Object.defineProperty(o.RTCPeerConnection.prototype,"localDescription",{get:function(){var e=s.get.apply(this);return""===e.type?e:a(this,e)}}),o.RTCPeerConnection.prototype.removeTrack=function(t){var r,n=this;if("closed"===n.signalingState)throw new DOMException("The RTCPeerConnection's signalingState is 'closed'.","InvalidStateError");if(!t._pc)throw new DOMException("Argument 1 of RTCPeerConnection.removeTrack does not implement interface RTCRtpSender.","TypeError");if(!(t._pc===n))throw new DOMException("Sender was not created by this connection.","InvalidAccessError");n._streams=n._streams||{},Object.keys(n._streams).forEach(function(e){n._streams[e].getTracks().find(function(e){return t.track===e})&&(r=n._streams[e])}),r&&(1===r.getTracks().length?n.removeStream(n._reverseStreams[r.id]):r.removeTrack(t.track),n.dispatchEvent(new Event("negotiationneeded")))}},shimPeerConnection:function(r){var e=c.detectBrowser(r);!r.RTCPeerConnection&&r.webkitRTCPeerConnection&&(r.RTCPeerConnection=function(e,t){return n("PeerConnection"),e&&e.iceTransportPolicy&&(e.iceTransports=e.iceTransportPolicy),new r.webkitRTCPeerConnection(e,t)},r.RTCPeerConnection.prototype=r.webkitRTCPeerConnection.prototype,r.webkitRTCPeerConnection.generateCertificate&&Object.defineProperty(r.RTCPeerConnection,"generateCertificate",{get:function(){return r.webkitRTCPeerConnection.generateCertificate}}));var s=r.RTCPeerConnection.prototype.getStats;r.RTCPeerConnection.prototype.getStats=function(e,t,r){var n=this,i=arguments;if(0<arguments.length&&"function"==typeof e)return s.apply(this,arguments);if(0===s.length&&(0===arguments.length||"function"!=typeof e))return s.apply(this,[]);var a=function(e){var n={};return e.result().forEach(function(t){var r={id:t.id,timestamp:t.timestamp,type:{localcandidate:"local-candidate",remotecandidate:"remote-candidate"}[t.type]||t.type};t.names().forEach(function(e){r[e]=t.stat(e)}),n[r.id]=r}),n},o=function(t){return new Map(Object.keys(t).map(function(e){return[e,t[e]]}))};if(2<=arguments.length){return s.apply(this,[function(e){i[1](o(a(e)))},e])}return new Promise(function(t,e){s.apply(n,[function(e){t(o(a(e)))},e])}).then(t,r)},e.version<51&&["setLocalDescription","setRemoteDescription","addIceCandidate"].forEach(function(e){var i=r.RTCPeerConnection.prototype[e];r.RTCPeerConnection.prototype[e]=function(){var r=arguments,n=this,e=new Promise(function(e,t){i.apply(n,[r[0],e,t])});return r.length<2?e:e.then(function(){r[1].apply(null,[])},function(e){3<=r.length&&r[2].apply(null,[e])})}}),e.version<52&&["createOffer","createAnswer"].forEach(function(e){var i=r.RTCPeerConnection.prototype[e];r.RTCPeerConnection.prototype[e]=function(){var r=this;if(arguments.length<1||1===arguments.length&&"object"==typeof arguments[0]){var n=1===arguments.length?arguments[0]:void 0;return new Promise(function(e,t){i.apply(r,[e,t,n])})}return i.apply(this,arguments)}}),["setLocalDescription","setRemoteDescription","addIceCandidate"].forEach(function(e){var t=r.RTCPeerConnection.prototype[e];r.RTCPeerConnection.prototype[e]=function(){return arguments[0]=new("addIceCandidate"===e?r.RTCIceCandidate:r.RTCSessionDescription)(arguments[0]),t.apply(this,arguments)}});var t=r.RTCPeerConnection.prototype.addIceCandidate;r.RTCPeerConnection.prototype.addIceCandidate=function(){return arguments[0]?t.apply(this,arguments):(arguments[1]&&arguments[1].apply(null),Promise.resolve())}},fixNegotiationNeeded:function(e){c.wrapPeerConnectionEvent(e,"negotiationneeded",function(e){if("stable"===e.target.signalingState)return e})},shimGetDisplayMedia:function(e,r){"getDisplayMedia"in e.navigator||("function"==typeof r?navigator.getDisplayMedia=function(t){return r(t).then(function(e){return t.video={mandatory:{chromeMediaSource:"desktop",chromeMediaSourceId:e,maxFrameRate:t.video.frameRate||3}},navigator.mediaDevices.getUserMedia(t)})}:console.error("shimGetDisplayMedia: getSourceId argument is not a function"))}}},{"../utils.js":14,"./getusermedia":6}],6:[function(e,t,r){"use strict";var a=e("../utils.js"),d=a.log;t.exports=function(e){var o=a.detectBrowser(e),s=e&&e.navigator,c=function(i){if("object"!=typeof i||i.mandatory||i.optional)return i;var a={};return Object.keys(i).forEach(function(t){if("require"!==t&&"advanced"!==t&&"mediaSource"!==t){var r="object"==typeof i[t]?i[t]:{ideal:i[t]};void 0!==r.exact&&"number"==typeof r.exact&&(r.min=r.max=r.exact);var n=function(e,t){return e?e+t.charAt(0).toUpperCase()+t.slice(1):"deviceId"===t?"sourceId":t};if(void 0!==r.ideal){a.optional=a.optional||[];var e={};"number"==typeof r.ideal?(e[n("min",t)]=r.ideal,a.optional.push(e),(e={})[n("max",t)]=r.ideal):e[n("",t)]=r.ideal,a.optional.push(e)}void 0!==r.exact&&"number"!=typeof r.exact?(a.mandatory=a.mandatory||{},a.mandatory[n("",t)]=r.exact):["min","max"].forEach(function(e){void 0!==r[e]&&(a.mandatory=a.mandatory||{},a.mandatory[n(e,t)]=r[e])})}}),i.advanced&&(a.optional=(a.optional||[]).concat(i.advanced)),a},n=function(r,n){if(61<=o.version)return n(r);if((r=JSON.parse(JSON.stringify(r)))&&"object"==typeof r.audio){var e=function(e,t,r){t in e&&!(r in e)&&(e[r]=e[t],delete e[t])};e((r=JSON.parse(JSON.stringify(r))).audio,"autoGainControl","googAutoGainControl"),e(r.audio,"noiseSuppression","googNoiseSuppression"),r.audio=c(r.audio)}if(r&&"object"==typeof r.video){var i=r.video.facingMode;i=i&&("object"==typeof i?i:{ideal:i});var a,t=o.version<66;if(i&&("user"===i.exact||"environment"===i.exact||"user"===i.ideal||"environment"===i.ideal)&&(!s.mediaDevices.getSupportedConstraints||!s.mediaDevices.getSupportedConstraints().facingMode||t))if(delete r.video.facingMode,"environment"===i.exact||"environment"===i.ideal?a=["back","rear"]:"user"!==i.exact&&"user"!==i.ideal||(a=["front"]),a)return s.mediaDevices.enumerateDevices().then(function(e){var t=(e=e.filter(function(e){return"videoinput"===e.kind})).find(function(t){return a.some(function(e){return-1!==t.label.toLowerCase().indexOf(e)})});return!t&&e.length&&-1!==a.indexOf("back")&&(t=e[e.length-1]),t&&(r.video.deviceId=i.exact?{exact:t.deviceId}:{ideal:t.deviceId}),r.video=c(r.video),d("chrome: "+JSON.stringify(r)),n(r)});r.video=c(r.video)}return d("chrome: "+JSON.stringify(r)),n(r)},i=function(e){return 64<=o.version?e:{name:{PermissionDeniedError:"NotAllowedError",PermissionDismissedError:"NotAllowedError",InvalidStateError:"NotAllowedError",DevicesNotFoundError:"NotFoundError",ConstraintNotSatisfiedError:"OverconstrainedError",TrackStartError:"NotReadableError",MediaDeviceFailedDueToShutdown:"NotAllowedError",MediaDeviceKillSwitchOn:"NotAllowedError",TabCaptureError:"AbortError",ScreenCaptureError:"AbortError",DeviceCaptureError:"AbortError"}[e.name]||e.name,message:e.message,constraint:e.constraint||e.constraintName,toString:function(){return this.name+(this.message&&": ")+this.message}}};s.getUserMedia=function(e,t,r){n(e,function(e){s.webkitGetUserMedia(e,t,function(e){r&&r(i(e))})})};var t=function(r){return new Promise(function(e,t){s.getUserMedia(r,e,t)})};if(s.mediaDevices||(s.mediaDevices={getUserMedia:t,enumerateDevices:function(){return new Promise(function(t){var r={audio:"audioinput",video:"videoinput"};return e.MediaStreamTrack.getSources(function(e){t(e.map(function(e){return{label:e.label,kind:r[e.kind],deviceId:e.id,groupId:""}}))})})},getSupportedConstraints:function(){return{deviceId:!0,echoCancellation:!0,facingMode:!0,frameRate:!0,height:!0,width:!0}}}),s.mediaDevices.getUserMedia){var r=s.mediaDevices.getUserMedia.bind(s.mediaDevices);s.mediaDevices.getUserMedia=function(e){return n(e,function(t){return r(t).then(function(e){if(t.audio&&!e.getAudioTracks().length||t.video&&!e.getVideoTracks().length)throw e.getTracks().forEach(function(e){e.stop()}),new DOMException("","NotFoundError");return e},function(e){return Promise.reject(i(e))})})}}else s.mediaDevices.getUserMedia=function(e){return t(e)};void 0===s.mediaDevices.addEventListener&&(s.mediaDevices.addEventListener=function(){d("Dummy mediaDevices.addEventListener called.")}),void 0===s.mediaDevices.removeEventListener&&(s.mediaDevices.removeEventListener=function(){d("Dummy mediaDevices.removeEventListener called.")})}},{"../utils.js":14}],7:[function(e,t,r){"use strict";var u=e("sdp"),c=e("./utils");t.exports={shimRTCIceCandidate:function(t){if(t.RTCIceCandidate&&!(t.RTCIceCandidate&&"foundation"in t.RTCIceCandidate.prototype)){var i=t.RTCIceCandidate;t.RTCIceCandidate=function(e){if("object"==typeof e&&e.candidate&&0===e.candidate.indexOf("a=")&&((e=JSON.parse(JSON.stringify(e))).candidate=e.candidate.substr(2)),e.candidate&&e.candidate.length){var t=new i(e),r=u.parseCandidate(e.candidate),n=Object.assign(t,r);return n.toJSON=function(){return{candidate:n.candidate,sdpMid:n.sdpMid,sdpMLineIndex:n.sdpMLineIndex,usernameFragment:n.usernameFragment}},n}return new i(e)},t.RTCIceCandidate.prototype=i.prototype,c.wrapPeerConnectionEvent(t,"icecandidate",function(e){return e.candidate&&Object.defineProperty(e,"candidate",{value:new t.RTCIceCandidate(e.candidate),writable:"false"}),e})}},shimCreateObjectURL:function(e){var t=e&&e.URL;if("object"==typeof e&&e.HTMLMediaElement&&"srcObject"in e.HTMLMediaElement.prototype&&t.createObjectURL&&t.revokeObjectURL){var r=t.createObjectURL.bind(t),n=t.revokeObjectURL.bind(t),i=new Map,a=0;t.createObjectURL=function(e){if("getTracks"in e){var t="polyblob:"+ ++a;return i.set(t,e),c.deprecated("URL.createObjectURL(stream)","elem.srcObject = stream"),t}return r(e)},t.revokeObjectURL=function(e){n(e),i.delete(e)};var o=Object.getOwnPropertyDescriptor(e.HTMLMediaElement.prototype,"src");Object.defineProperty(e.HTMLMediaElement.prototype,"src",{get:function(){return o.get.apply(this)},set:function(e){return this.srcObject=i.get(e)||null,o.set.apply(this,[e])}});var s=e.HTMLMediaElement.prototype.setAttribute;e.HTMLMediaElement.prototype.setAttribute=function(){return 2===arguments.length&&"src"===(""+arguments[0]).toLowerCase()&&(this.srcObject=i.get(arguments[1])||null),s.apply(this,arguments)}}},shimMaxMessageSize:function(e){if(!e.RTCSctpTransport&&e.RTCPeerConnection){var d=c.detectBrowser(e);"sctp"in e.RTCPeerConnection.prototype||Object.defineProperty(e.RTCPeerConnection.prototype,"sctp",{get:function(){return void 0===this._sctp?null:this._sctp}});var p=e.RTCPeerConnection.prototype.setRemoteDescription;e.RTCPeerConnection.prototype.setRemoteDescription=function(){var e,t,r,n;if(this._sctp=null,r=arguments[0],(n=u.splitSections(r.sdp)).shift(),n.some(function(e){var t=u.parseMLine(e);return t&&"application"===t.kind&&-1!==t.protocol.indexOf("SCTP")})){var i,a=function(e){var t=e.sdp.match(/mozilla...THIS_IS_SDPARTA-(\d+)/);if(null===t||t.length<2)return-1;var r=parseInt(t[1],10);return r!=r?-1:r}(arguments[0]),o=(e=a,t=65536,"firefox"===d.browser&&(t=d.version<57?-1===e?16384:2147483637:d.version<60?57===d.version?65535:65536:2147483637),t),s=function(e,t){var r=65536;"firefox"===d.browser&&57===d.version&&(r=65535);var n=u.matchPrefix(e.sdp,"a=max-message-size:");return 0<n.length?r=parseInt(n[0].substr(19),10):"firefox"===d.browser&&-1!==t&&(r=2147483637),r}(arguments[0],a);i=0===o&&0===s?Number.POSITIVE_INFINITY:0===o||0===s?Math.max(o,s):Math.min(o,s);var c={};Object.defineProperty(c,"maxMessageSize",{get:function(){return i}}),this._sctp=c}return p.apply(this,arguments)}}},shimSendThrowTypeError:function(e){if(e.RTCPeerConnection&&"createDataChannel"in e.RTCPeerConnection.prototype){var t=e.RTCPeerConnection.prototype.createDataChannel;e.RTCPeerConnection.prototype.createDataChannel=function(){var e=t.apply(this,arguments);return r(e,this),e},c.wrapPeerConnectionEvent(e,"datachannel",function(e){return r(e.channel,e.target),e})}function r(r,n){var i=r.send;r.send=function(){var e=arguments[0],t=e.length||e.size||e.byteLength;if("open"===r.readyState&&n.sctp&&t>n.sctp.maxMessageSize)throw new TypeError("Message too large (can send a maximum of "+n.sctp.maxMessageSize+" bytes)");return i.apply(r,arguments)}}}}},{"./utils":14,sdp:2}],8:[function(e,t,r){"use strict";var i=e("../utils"),a=e("./filtericeservers"),o=e("rtcpeerconnection-shim");t.exports={shimGetUserMedia:e("./getusermedia"),shimPeerConnection:function(e){var t=i.detectBrowser(e);if(e.RTCIceGatherer&&(e.RTCIceCandidate||(e.RTCIceCandidate=function(e){return e}),e.RTCSessionDescription||(e.RTCSessionDescription=function(e){return e}),t.version<15025)){var r=Object.getOwnPropertyDescriptor(e.MediaStreamTrack.prototype,"enabled");Object.defineProperty(e.MediaStreamTrack.prototype,"enabled",{set:function(e){r.set.call(this,e);var t=new Event("enabled");t.enabled=e,this.dispatchEvent(t)}})}!e.RTCRtpSender||"dtmf"in e.RTCRtpSender.prototype||Object.defineProperty(e.RTCRtpSender.prototype,"dtmf",{get:function(){return void 0===this._dtmf&&("audio"===this.track.kind?this._dtmf=new e.RTCDtmfSender(this):"video"===this.track.kind&&(this._dtmf=null)),this._dtmf}}),e.RTCDtmfSender&&!e.RTCDTMFSender&&(e.RTCDTMFSender=e.RTCDtmfSender);var n=o(e,t.version);e.RTCPeerConnection=function(e){return e&&e.iceServers&&(e.iceServers=a(e.iceServers)),new n(e)},e.RTCPeerConnection.prototype=n.prototype},shimReplaceTrack:function(e){!e.RTCRtpSender||"replaceTrack"in e.RTCRtpSender.prototype||(e.RTCRtpSender.prototype.replaceTrack=e.RTCRtpSender.prototype.setTrack)}}},{"../utils":14,"./filtericeservers":9,"./getusermedia":10,"rtcpeerconnection-shim":1}],9:[function(e,t,r){"use strict";var a=e("../utils");t.exports=function(e,n){var i=!1;return(e=JSON.parse(JSON.stringify(e))).filter(function(e){if(e&&(e.urls||e.url)){var t=e.urls||e.url;e.url&&!e.urls&&a.deprecated("RTCIceServer.url","RTCIceServer.urls");var r="string"==typeof t;return r&&(t=[t]),t=t.filter(function(e){return 0===e.indexOf("turn:")&&-1!==e.indexOf("transport=udp")&&-1===e.indexOf("turn:[")&&!i?i=!0:0===e.indexOf("stun:")&&14393<=n&&-1===e.indexOf("?transport=udp")}),delete e.url,e.urls=r?t[0]:t,!!t.length}})}},{"../utils":14}],10:[function(e,t,r){"use strict";t.exports=function(e){var t=e&&e.navigator,r=t.mediaDevices.getUserMedia.bind(t.mediaDevices);t.mediaDevices.getUserMedia=function(e){return r(e).catch(function(e){return Promise.reject({name:{PermissionDeniedError:"NotAllowedError"}[(t=e).name]||t.name,message:t.message,constraint:t.constraint,toString:function(){return this.name}});var t})}}},{}],11:[function(e,t,r){"use strict";var n=e("../utils");t.exports={shimGetUserMedia:e("./getusermedia"),shimOnTrack:function(e){"object"!=typeof e||!e.RTCPeerConnection||"ontrack"in e.RTCPeerConnection.prototype||Object.defineProperty(e.RTCPeerConnection.prototype,"ontrack",{get:function(){return this._ontrack},set:function(e){this._ontrack&&(this.removeEventListener("track",this._ontrack),this.removeEventListener("addstream",this._ontrackpoly)),this.addEventListener("track",this._ontrack=e),this.addEventListener("addstream",this._ontrackpoly=function(r){r.stream.getTracks().forEach(function(e){var t=new Event("track");t.track=e,t.receiver={track:e},t.transceiver={receiver:t.receiver},t.streams=[r.stream],this.dispatchEvent(t)}.bind(this))}.bind(this))},enumerable:!0,configurable:!0}),"object"==typeof e&&e.RTCTrackEvent&&"receiver"in e.RTCTrackEvent.prototype&&!("transceiver"in e.RTCTrackEvent.prototype)&&Object.defineProperty(e.RTCTrackEvent.prototype,"transceiver",{get:function(){return{receiver:this.receiver}}})},shimSourceObject:function(e){"object"==typeof e&&(!e.HTMLMediaElement||"srcObject"in e.HTMLMediaElement.prototype||Object.defineProperty(e.HTMLMediaElement.prototype,"srcObject",{get:function(){return this.mozSrcObject},set:function(e){this.mozSrcObject=e}}))},shimPeerConnection:function(s){var c=n.detectBrowser(s);if("object"==typeof s&&(s.RTCPeerConnection||s.mozRTCPeerConnection)){s.RTCPeerConnection||(s.RTCPeerConnection=function(e,t){if(c.version<38&&e&&e.iceServers){for(var r=[],n=0;n<e.iceServers.length;n++){var i=e.iceServers[n];if(i.hasOwnProperty("urls"))for(var a=0;a<i.urls.length;a++){var o={url:i.urls[a]};0===i.urls[a].indexOf("turn")&&(o.username=i.username,o.credential=i.credential),r.push(o)}else r.push(e.iceServers[n])}e.iceServers=r}return new s.mozRTCPeerConnection(e,t)},s.RTCPeerConnection.prototype=s.mozRTCPeerConnection.prototype,s.mozRTCPeerConnection.generateCertificate&&Object.defineProperty(s.RTCPeerConnection,"generateCertificate",{get:function(){return s.mozRTCPeerConnection.generateCertificate}}),s.RTCSessionDescription=s.mozRTCSessionDescription,s.RTCIceCandidate=s.mozRTCIceCandidate),["setLocalDescription","setRemoteDescription","addIceCandidate"].forEach(function(e){var t=s.RTCPeerConnection.prototype[e];s.RTCPeerConnection.prototype[e]=function(){return arguments[0]=new("addIceCandidate"===e?s.RTCIceCandidate:s.RTCSessionDescription)(arguments[0]),t.apply(this,arguments)}});var e=s.RTCPeerConnection.prototype.addIceCandidate;s.RTCPeerConnection.prototype.addIceCandidate=function(){return arguments[0]?e.apply(this,arguments):(arguments[1]&&arguments[1].apply(null),Promise.resolve())};var a={inboundrtp:"inbound-rtp",outboundrtp:"outbound-rtp",candidatepair:"candidate-pair",localcandidate:"local-candidate",remotecandidate:"remote-candidate"},r=s.RTCPeerConnection.prototype.getStats;s.RTCPeerConnection.prototype.getStats=function(e,i,t){return r.apply(this,[e||null]).then(function(r){var t,n;if(c.version<48&&(t=r,n=new Map,Object.keys(t).forEach(function(e){n.set(e,t[e]),n[e]=t[e]}),r=n),c.version<53&&!i)try{r.forEach(function(e){e.type=a[e.type]||e.type})}catch(e){if("TypeError"!==e.name)throw e;r.forEach(function(e,t){r.set(t,Object.assign({},e,{type:a[e.type]||e.type}))})}return r}).then(i,t)}}},shimSenderGetStats:function(e){if("object"==typeof e&&e.RTCPeerConnection&&e.RTCRtpSender&&!(e.RTCRtpSender&&"getStats"in e.RTCRtpSender.prototype)){var r=e.RTCPeerConnection.prototype.getSenders;r&&(e.RTCPeerConnection.prototype.getSenders=function(){var t=this,e=r.apply(t,[]);return e.forEach(function(e){e._pc=t}),e});var t=e.RTCPeerConnection.prototype.addTrack;t&&(e.RTCPeerConnection.prototype.addTrack=function(){var e=t.apply(this,arguments);return e._pc=this,e}),e.RTCRtpSender.prototype.getStats=function(){return this.track?this._pc.getStats(this.track):Promise.resolve(new Map)}}},shimReceiverGetStats:function(e){if("object"==typeof e&&e.RTCPeerConnection&&e.RTCRtpSender&&!(e.RTCRtpSender&&"getStats"in e.RTCRtpReceiver.prototype)){var r=e.RTCPeerConnection.prototype.getReceivers;r&&(e.RTCPeerConnection.prototype.getReceivers=function(){var t=this,e=r.apply(t,[]);return e.forEach(function(e){e._pc=t}),e}),n.wrapPeerConnectionEvent(e,"track",function(e){return e.receiver._pc=e.srcElement,e}),e.RTCRtpReceiver.prototype.getStats=function(){return this._pc.getStats(this.track)}}},shimRemoveStream:function(e){!e.RTCPeerConnection||"removeStream"in e.RTCPeerConnection.prototype||(e.RTCPeerConnection.prototype.removeStream=function(t){var r=this;n.deprecated("removeStream","removeTrack"),this.getSenders().forEach(function(e){e.track&&-1!==t.getTracks().indexOf(e.track)&&r.removeTrack(e)})})},shimRTCDataChannel:function(e){e.DataChannel&&!e.RTCDataChannel&&(e.RTCDataChannel=e.DataChannel)},shimGetDisplayMedia:function(e,r){"getDisplayMedia"in e.navigator||(navigator.getDisplayMedia=function(e){if(!e||!e.video){var t=new DOMException("getDisplayMedia without video constraints is undefined");return t.name="NotFoundError",t.code=8,Promise.reject(t)}return!0===e.video?e.video={mediaSource:r}:e.video.mediaSource=r,navigator.mediaDevices.getUserMedia(e)})}}},{"../utils":14,"./getusermedia":12}],12:[function(e,t,r){"use strict";var f=e("../utils"),l=f.log;t.exports=function(e){var i=f.detectBrowser(e),a=e&&e.navigator,t=e&&e.MediaStreamTrack,o=function(e){return{name:{InternalError:"NotReadableError",NotSupportedError:"TypeError",PermissionDeniedError:"NotAllowedError",SecurityError:"NotAllowedError"}[e.name]||e.name,message:{"The operation is insecure.":"The request is not allowed by the user agent or the platform in the current context."}[e.message]||e.message,constraint:e.constraint,toString:function(){return this.name+(this.message&&": ")+this.message}}},n=function(e,t,r){var n=function(n){if("object"!=typeof n||n.require)return n;var i=[];return Object.keys(n).forEach(function(e){if("require"!==e&&"advanced"!==e&&"mediaSource"!==e){var t=n[e]="object"==typeof n[e]?n[e]:{ideal:n[e]};if(void 0===t.min&&void 0===t.max&&void 0===t.exact||i.push(e),void 0!==t.exact&&("number"==typeof t.exact?t.min=t.max=t.exact:n[e]=t.exact,delete t.exact),void 0!==t.ideal){n.advanced=n.advanced||[];var r={};"number"==typeof t.ideal?r[e]={min:t.ideal,max:t.ideal}:r[e]=t.ideal,n.advanced.push(r),delete t.ideal,Object.keys(t).length||delete n[e]}}}),i.length&&(n.require=i),n};return e=JSON.parse(JSON.stringify(e)),i.version<38&&(l("spec: "+JSON.stringify(e)),e.audio&&(e.audio=n(e.audio)),e.video&&(e.video=n(e.video)),l("ff37: "+JSON.stringify(e))),a.mozGetUserMedia(e,t,function(e){r(o(e))})};if(a.mediaDevices||(a.mediaDevices={getUserMedia:function(r){return new Promise(function(e,t){n(r,e,t)})},addEventListener:function(){},removeEventListener:function(){}}),a.mediaDevices.enumerateDevices=a.mediaDevices.enumerateDevices||function(){return new Promise(function(e){e([{kind:"audioinput",deviceId:"default",label:"",groupId:""},{kind:"videoinput",deviceId:"default",label:"",groupId:""}])})},i.version<41){var r=a.mediaDevices.enumerateDevices.bind(a.mediaDevices);a.mediaDevices.enumerateDevices=function(){return r().then(void 0,function(e){if("NotFoundError"===e.name)return[];throw e})}}if(i.version<49){var s=a.mediaDevices.getUserMedia.bind(a.mediaDevices);a.mediaDevices.getUserMedia=function(t){return s(t).then(function(e){if(t.audio&&!e.getAudioTracks().length||t.video&&!e.getVideoTracks().length)throw e.getTracks().forEach(function(e){e.stop()}),new DOMException("The object can not be found here.","NotFoundError");return e},function(e){return Promise.reject(o(e))})}}if(!(55<i.version&&"autoGainControl"in a.mediaDevices.getSupportedConstraints())){var c=function(e,t,r){t in e&&!(r in e)&&(e[r]=e[t],delete e[t])},d=a.mediaDevices.getUserMedia.bind(a.mediaDevices);if(a.mediaDevices.getUserMedia=function(e){return"object"==typeof e&&"object"==typeof e.audio&&(e=JSON.parse(JSON.stringify(e)),c(e.audio,"autoGainControl","mozAutoGainControl"),c(e.audio,"noiseSuppression","mozNoiseSuppression")),d(e)},t&&t.prototype.getSettings){var p=t.prototype.getSettings;t.prototype.getSettings=function(){var e=p.apply(this,arguments);return c(e,"mozAutoGainControl","autoGainControl"),c(e,"mozNoiseSuppression","noiseSuppression"),e}}if(t&&t.prototype.applyConstraints){var u=t.prototype.applyConstraints;t.prototype.applyConstraints=function(e){return"audio"===this.kind&&"object"==typeof e&&(e=JSON.parse(JSON.stringify(e)),c(e,"autoGainControl","mozAutoGainControl"),c(e,"noiseSuppression","mozNoiseSuppression")),u.apply(this,[e])}}}a.getUserMedia=function(e,t,r){if(i.version<44)return n(e,t,r);f.deprecated("navigator.getUserMedia","navigator.mediaDevices.getUserMedia"),a.mediaDevices.getUserMedia(e).then(t,r)}}},{"../utils":14}],13:[function(e,t,r){"use strict";var o=e("../utils");t.exports={shimLocalStreamsAPI:function(e){if("object"==typeof e&&e.RTCPeerConnection){if("getLocalStreams"in e.RTCPeerConnection.prototype||(e.RTCPeerConnection.prototype.getLocalStreams=function(){return this._localStreams||(this._localStreams=[]),this._localStreams}),"getStreamById"in e.RTCPeerConnection.prototype||(e.RTCPeerConnection.prototype.getStreamById=function(t){var r=null;return this._localStreams&&this._localStreams.forEach(function(e){e.id===t&&(r=e)}),this._remoteStreams&&this._remoteStreams.forEach(function(e){e.id===t&&(r=e)}),r}),!("addStream"in e.RTCPeerConnection.prototype)){var n=e.RTCPeerConnection.prototype.addTrack;e.RTCPeerConnection.prototype.addStream=function(t){this._localStreams||(this._localStreams=[]),-1===this._localStreams.indexOf(t)&&this._localStreams.push(t);var r=this;t.getTracks().forEach(function(e){n.call(r,e,t)})},e.RTCPeerConnection.prototype.addTrack=function(e,t){return t&&(this._localStreams?-1===this._localStreams.indexOf(t)&&this._localStreams.push(t):this._localStreams=[t]),n.call(this,e,t)}}"removeStream"in e.RTCPeerConnection.prototype||(e.RTCPeerConnection.prototype.removeStream=function(e){this._localStreams||(this._localStreams=[]);var t=this._localStreams.indexOf(e);if(-1!==t){this._localStreams.splice(t,1);var r=this,n=e.getTracks();this.getSenders().forEach(function(e){-1!==n.indexOf(e.track)&&r.removeTrack(e)})}})}},shimRemoteStreamsAPI:function(e){if("object"==typeof e&&e.RTCPeerConnection&&("getRemoteStreams"in e.RTCPeerConnection.prototype||(e.RTCPeerConnection.prototype.getRemoteStreams=function(){return this._remoteStreams?this._remoteStreams:[]}),!("onaddstream"in e.RTCPeerConnection.prototype))){Object.defineProperty(e.RTCPeerConnection.prototype,"onaddstream",{get:function(){return this._onaddstream},set:function(e){this._onaddstream&&this.removeEventListener("addstream",this._onaddstream),this.addEventListener("addstream",this._onaddstream=e)}});var t=e.RTCPeerConnection.prototype.setRemoteDescription;e.RTCPeerConnection.prototype.setRemoteDescription=function(){var r=this;return this._onaddstreampoly||this.addEventListener("track",this._onaddstreampoly=function(e){e.streams.forEach(function(e){if(r._remoteStreams||(r._remoteStreams=[]),!(0<=r._remoteStreams.indexOf(e))){r._remoteStreams.push(e);var t=new Event("addstream");t.stream=e,r.dispatchEvent(t)}})}),t.apply(r,arguments)}}},shimCallbacksAPI:function(e){if("object"==typeof e&&e.RTCPeerConnection){var t=e.RTCPeerConnection.prototype,i=t.createOffer,a=t.createAnswer,o=t.setLocalDescription,s=t.setRemoteDescription,c=t.addIceCandidate;t.createOffer=function(e,t){var r=2<=arguments.length?arguments[2]:e,n=i.apply(this,[r]);return t?(n.then(e,t),Promise.resolve()):n},t.createAnswer=function(e,t){var r=2<=arguments.length?arguments[2]:e,n=a.apply(this,[r]);return t?(n.then(e,t),Promise.resolve()):n};var r=function(e,t,r){var n=o.apply(this,[e]);return r?(n.then(t,r),Promise.resolve()):n};t.setLocalDescription=r,r=function(e,t,r){var n=s.apply(this,[e]);return r?(n.then(t,r),Promise.resolve()):n},t.setRemoteDescription=r,r=function(e,t,r){var n=c.apply(this,[e]);return r?(n.then(t,r),Promise.resolve()):n},t.addIceCandidate=r}},shimGetUserMedia:function(e){var n=e&&e.navigator;n.getUserMedia||(n.webkitGetUserMedia?n.getUserMedia=n.webkitGetUserMedia.bind(n):n.mediaDevices&&n.mediaDevices.getUserMedia&&(n.getUserMedia=function(e,t,r){n.mediaDevices.getUserMedia(e).then(t,r)}.bind(n)))},shimRTCIceServerUrls:function(e){var a=e.RTCPeerConnection;e.RTCPeerConnection=function(e,t){if(e&&e.iceServers){for(var r=[],n=0;n<e.iceServers.length;n++){var i=e.iceServers[n];!i.hasOwnProperty("urls")&&i.hasOwnProperty("url")?(o.deprecated("RTCIceServer.url","RTCIceServer.urls"),(i=JSON.parse(JSON.stringify(i))).urls=i.url,delete i.url,r.push(i)):r.push(e.iceServers[n])}e.iceServers=r}return new a(e,t)},e.RTCPeerConnection.prototype=a.prototype,"generateCertificate"in e.RTCPeerConnection&&Object.defineProperty(e.RTCPeerConnection,"generateCertificate",{get:function(){return a.generateCertificate}})},shimTrackEventTransceiver:function(e){"object"==typeof e&&e.RTCPeerConnection&&"receiver"in e.RTCTrackEvent.prototype&&!e.RTCTransceiver&&Object.defineProperty(e.RTCTrackEvent.prototype,"transceiver",{get:function(){return{receiver:this.receiver}}})},shimCreateOfferLegacy:function(e){var i=e.RTCPeerConnection.prototype.createOffer;e.RTCPeerConnection.prototype.createOffer=function(e){var t=this;if(e){void 0!==e.offerToReceiveAudio&&(e.offerToReceiveAudio=!!e.offerToReceiveAudio);var r=t.getTransceivers().find(function(e){return e.sender.track&&"audio"===e.sender.track.kind});!1===e.offerToReceiveAudio&&r?"sendrecv"===r.direction?r.setDirection?r.setDirection("sendonly"):r.direction="sendonly":"recvonly"===r.direction&&(r.setDirection?r.setDirection("inactive"):r.direction="inactive"):!0!==e.offerToReceiveAudio||r||t.addTransceiver("audio"),void 0!==e.offerToReceiveVideo&&(e.offerToReceiveVideo=!!e.offerToReceiveVideo);var n=t.getTransceivers().find(function(e){return e.sender.track&&"video"===e.sender.track.kind});!1===e.offerToReceiveVideo&&n?"sendrecv"===n.direction?n.setDirection("sendonly"):"recvonly"===n.direction&&n.setDirection("inactive"):!0!==e.offerToReceiveVideo||n||t.addTransceiver("video")}return i.apply(t,arguments)}}}},{"../utils":14}],14:[function(e,t,r){"use strict";var n=!0,i=!0;function a(e,t,r){var n=e.match(t);return n&&n.length>=r&&parseInt(n[r],10)}t.exports={extractVersion:a,wrapPeerConnectionEvent:function(e,n,i){if(e.RTCPeerConnection){var t=e.RTCPeerConnection.prototype,a=t.addEventListener;t.addEventListener=function(e,r){if(e!==n)return a.apply(this,arguments);var t=function(e){var t=i(e);t&&r(t)};return this._eventMap=this._eventMap||{},this._eventMap[r]=t,a.apply(this,[e,t])};var o=t.removeEventListener;t.removeEventListener=function(e,t){if(e!==n||!this._eventMap||!this._eventMap[t])return o.apply(this,arguments);var r=this._eventMap[t];return delete this._eventMap[t],o.apply(this,[e,r])},Object.defineProperty(t,"on"+n,{get:function(){return this["_on"+n]},set:function(e){this["_on"+n]&&(this.removeEventListener(n,this["_on"+n]),delete this["_on"+n]),e&&this.addEventListener(n,this["_on"+n]=e)},enumerable:!0,configurable:!0})}},disableLog:function(e){return"boolean"!=typeof e?new Error("Argument type: "+typeof e+". Please use a boolean."):(n=e)?"adapter.js logging disabled":"adapter.js logging enabled"},disableWarnings:function(e){return"boolean"!=typeof e?new Error("Argument type: "+typeof e+". Please use a boolean."):(i=!e,"adapter.js deprecation warnings "+(e?"disabled":"enabled"))},log:function(){if("object"==typeof window){if(n)return;"undefined"!=typeof console&&"function"==typeof console.log&&console.log.apply(console,arguments)}},deprecated:function(e,t){i&&console.warn(e+" is deprecated, please use "+t+" instead.")},detectBrowser:function(e){var t=e&&e.navigator,r={browser:null,version:null};if(void 0===e||!e.navigator)return r.browser="Not a browser.",r;if(t.mozGetUserMedia)r.browser="firefox",r.version=a(t.userAgent,/Firefox\/(\d+)\./,1);else if(t.webkitGetUserMedia)r.browser="chrome",r.version=a(t.userAgent,/Chrom(e|ium)\/(\d+)\./,2);else if(t.mediaDevices&&t.userAgent.match(/Edge\/(\d+).(\d+)$/))r.browser="edge",r.version=a(t.userAgent,/Edge\/(\d+).(\d+)$/,2);else{if(!e.RTCPeerConnection||!t.userAgent.match(/AppleWebKit\/(\d+)\./))return r.browser="Not a supported browser.",r;r.browser="safari",r.version=a(t.userAgent,/AppleWebKit\/(\d+)\./,1)}return r}}},{}]},{},[3])(3)});

// List of sessions
Janus.sessions = {};

Janus.isExtensionEnabled = function() {
	if(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
		// No need for the extension, getDisplayMedia is supported
		return true;
	}
	if(window.navigator.userAgent.match('Chrome')) {
		var chromever = parseInt(window.navigator.userAgent.match(/Chrome\/(.*) /)[1], 10);
		var maxver = 33;
		if(window.navigator.userAgent.match('Linux'))
			maxver = 35;	// "known" crash in chrome 34 and 35 on linux
		if(chromever >= 26 && chromever <= maxver) {
			// Older versions of Chrome don't support this extension-based approach, so lie
			return true;
		}
		return Janus.extension.isInstalled();
	} else {
		// Firefox and others, no need for the extension (but this doesn't mean it will work)
		return true;
	}
};

var defaultExtension = {
	// Screensharing Chrome Extension ID
	extensionId: 'hapfgfdkleiggjjpfpenajgdnfckjpaj',
	isInstalled: function() { return document.querySelector('#janus-extension-installed') !== null; },
	getScreen: function (callback) {
		var pending = window.setTimeout(function () {
			var error = new Error('NavigatorUserMediaError');
			error.name = 'The required Chrome extension is not installed: click <a href="#">here</a> to install it. (NOTE: this will need you to refresh the page)';
			return callback(error);
		}, 1000);
		this.cache[pending] = callback;
		window.postMessage({ type: 'janusGetScreen', id: pending }, '*');
	},
	init: function () {
		var cache = {};
		this.cache = cache;
		// Wait for events from the Chrome Extension
		window.addEventListener('message', function (event) {
			if(event.origin != window.location.origin)
				return;
			if(event.data.type == 'janusGotScreen' && cache[event.data.id]) {
				var callback = cache[event.data.id];
				delete cache[event.data.id];

				if (event.data.sourceId === '') {
					// user canceled
					var error = new Error('NavigatorUserMediaError');
					error.name = 'You cancelled the request for permission, giving up...';
					callback(error);
				} else {
					callback(null, event.data.sourceId);
				}
			} else if (event.data.type == 'janusGetScreenPending') {
				console.log('clearing ', event.data.id);
				window.clearTimeout(event.data.id);
			}
		});
	}
};

Janus.useDefaultDependencies = function (deps) {
	var f = (deps && deps.fetch) || fetch;
	var p = (deps && deps.Promise) || Promise;
	var socketCls = (deps && deps.WebSocket) || WebSocket;

	return {
		newWebSocket: function(server, proto) { return new socketCls(server, proto); },
		extension: (deps && deps.extension) || defaultExtension,
		isArray: function(arr) { return Array.isArray(arr); },
		webRTCAdapter: (deps && deps.adapter) || adapter,
		httpAPICall: function(url, options) {
			var fetchOptions = {
				method: options.verb,
				headers: {
					'Accept': 'application/json, text/plain, */*'
				},
				cache: 'no-cache'
			};
			if(options.verb === "POST") {
				fetchOptions.headers['Content-Type'] = 'application/json';
			}
			if(options.withCredentials !== undefined) {
				fetchOptions.credentials = options.withCredentials === true ? 'include' : (options.withCredentials ? options.withCredentials : 'omit');
			}
			if(options.body) {
				fetchOptions.body = JSON.stringify(options.body);
			}

			var fetching = f(url, fetchOptions).catch(function(error) {
				return p.reject({message: 'Probably a network error, is the server down?', error: error});
			});

			/*
			 * fetch() does not natively support timeouts.
			 * Work around this by starting a timeout manually, and racing it agains the fetch() to see which thing resolves first.
			 */

			if(options.timeout) {
				var timeout = new p(function(resolve, reject) {
					var timerId = setTimeout(function() {
						clearTimeout(timerId);
						return reject({message: 'Request timed out', timeout: options.timeout});
					}, options.timeout);
				});
				fetching = p.race([fetching, timeout]);
			}

			fetching.then(function(response) {
				if(response.ok) {
					if(typeof(options.success) === typeof(Janus.noop)) {
						return response.json().then(function(parsed) {
							options.success(parsed);
						}).catch(function(error) {
							return p.reject({message: 'Failed to parse response body', error: error, response: response});
						});
					}
				}
				else {
					return p.reject({message: 'API call failed', response: response});
				}
			}).catch(function(error) {
				if(typeof(options.error) === typeof(Janus.noop)) {
					options.error(error.message || '<< internal error >>', error);
				}
			});

			return fetching;
		}
	}
};

Janus.useOldDependencies = function (deps) {
	var jq = (deps && deps.jQuery) || jQuery;
	var socketCls = (deps && deps.WebSocket) || WebSocket;
	return {
		newWebSocket: function(server, proto) { return new socketCls(server, proto); },
		isArray: function(arr) { return jq.isArray(arr); },
		extension: (deps && deps.extension) || defaultExtension,
		webRTCAdapter: (deps && deps.adapter) || adapter,
		httpAPICall: function(url, options) {
			var payload = options.body !== undefined ? {
				contentType: 'application/json',
				data: JSON.stringify(options.body)
			} : {};
			var credentials = options.withCredentials !== undefined ? {xhrFields: {withCredentials: options.withCredentials}} : {};

			return jq.ajax(jq.extend(payload, credentials, {
				url: url,
				type: options.verb,
				cache: false,
				dataType: 'json',
				async: options.async,
				timeout: options.timeout,
				success: function(result) {
					if(typeof(options.success) === typeof(Janus.noop)) {
						options.success(result);
					}
				},
				error: function(xhr, status, err) {
					if(typeof(options.error) === typeof(Janus.noop)) {
						options.error(status, err);
					}
				}
			}));
		}
	};
};

Janus.noop = function() {};

Janus.dataChanDefaultLabel = "JanusDataChannel";

// Note: in the future we may want to change this, e.g., as was
// attempted in https://github.com/meetecho/janus-gateway/issues/1670
Janus.endOfCandidates = null;

// Stop all tracks from a given stream
Janus.stopAllTracks = function(stream) {
	try {
		// Try a MediaStreamTrack.stop() for each track
		var tracks = stream.getTracks();
		for(var mst of tracks) {
			Janus.log(mst);
			if(mst) {
				mst.stop();
			}
		}
	} catch(e) {
		// Do nothing if this fails
	}
}

// Initialization
Janus.init = function(options) {
	options = options || {};
	options.callback = (typeof options.callback == "function") ? options.callback : Janus.noop;
	if(Janus.initDone) {
		// Already initialized
		options.callback();
	} else {
		if(typeof console == "undefined" || typeof console.log == "undefined") {
			console = { log: function() {} };
		}
		// Console logging (all debugging disabled by default)
		Janus.trace = Janus.noop;
		Janus.debug = Janus.noop;
		Janus.vdebug = Janus.noop;
		Janus.log = Janus.noop;
		Janus.warn = Janus.noop;
		Janus.error = Janus.noop;
		if(options.debug === true || options.debug === "all") {
			// Enable all debugging levels
			Janus.trace = console.trace.bind(console);
			Janus.debug = console.debug.bind(console);
			Janus.vdebug = console.debug.bind(console);
			Janus.log = console.log.bind(console);
			Janus.warn = console.warn.bind(console);
			Janus.error = console.error.bind(console);
		} else if(Array.isArray(options.debug)) {
			for(var d of options.debug) {
				switch(d) {
					case "trace":
						Janus.trace = console.trace.bind(console);
						break;
					case "debug":
						Janus.debug = console.debug.bind(console);
						break;
					case "vdebug":
						Janus.vdebug = console.debug.bind(console);
						break;
					case "log":
						Janus.log = console.log.bind(console);
						break;
					case "warn":
						Janus.warn = console.warn.bind(console);
						break;
					case "error":
						Janus.error = console.error.bind(console);
						break;
					default:
						console.error("Unknown debugging option '" + d + "' (supported: 'trace', 'debug', 'vdebug', 'log', warn', 'error')");
						break;
				}
			}
		}
		Janus.log("Initializing library");

		var usedDependencies = options.dependencies || Janus.useDefaultDependencies();
		Janus.isArray = usedDependencies.isArray;
		Janus.webRTCAdapter = usedDependencies.webRTCAdapter;
		Janus.httpAPICall = usedDependencies.httpAPICall;
		Janus.newWebSocket = usedDependencies.newWebSocket;
		Janus.extension = usedDependencies.extension;
		Janus.extension.init();

		// Helper method to enumerate devices
		Janus.listDevices = function(callback, config) {
			callback = (typeof callback == "function") ? callback : Janus.noop;
			if (config == null) config = { audio: true, video: true };
			if(Janus.isGetUserMediaAvailable()) {
				navigator.mediaDevices.getUserMedia(config)
				.then(function(stream) {
					navigator.mediaDevices.enumerateDevices().then(function(devices) {
						Janus.debug(devices);
						callback(devices);
						// Get rid of the now useless stream
						Janus.stopAllTracks(stream)
					});
				})
				.catch(function(err) {
					Janus.error(err);
					callback([]);
				});
			} else {
				Janus.warn("navigator.mediaDevices unavailable");
				callback([]);
			}
		};
		// Helper methods to attach/reattach a stream to a video element (previously part of adapter.js)
		Janus.attachMediaStream = function(element, stream) {
			try {
				element.srcObject = stream;
			} catch (e) {
				try {
					element.src = URL.createObjectURL(stream);
				} catch (e) {
					Janus.error("Error attaching stream to element");
				}
			}
		};
		Janus.reattachMediaStream = function(to, from) {
			try {
				to.srcObject = from.srcObject;
			} catch (e) {
				try {
					to.src = from.src;
				} catch (e) {
					Janus.error("Error reattaching stream to element");
				}
			}
		};
		// Detect tab close: make sure we don't loose existing onbeforeunload handlers
		// (note: for iOS we need to subscribe to a different event, 'pagehide', see
		// https://gist.github.com/thehunmonkgroup/6bee8941a49b86be31a787fe8f4b8cfe)
		var iOS = ['iPad', 'iPhone', 'iPod'].indexOf(navigator.platform) >= 0;
		var eventName = iOS ? 'pagehide' : 'beforeunload';
		var oldOBF = window["on" + eventName];
		window.addEventListener(eventName, function(event) {
			Janus.log("Closing window");
			for(var s in Janus.sessions) {
				if(Janus.sessions[s] && Janus.sessions[s].destroyOnUnload) {
					Janus.log("Destroying session " + s);
					Janus.sessions[s].destroy({unload: true, notifyDestroyed: false});
				}
			}
			if(oldOBF && typeof oldOBF == "function") {
				oldOBF();
			}
		});
		// If this is a Safari Technology Preview, check if VP8 is supported
		Janus.safariVp8 = false;
		if(Janus.webRTCAdapter.browserDetails.browser === 'safari' &&
				Janus.webRTCAdapter.browserDetails.version >= 605) {
			// Let's see if RTCRtpSender.getCapabilities() is there
			if(RTCRtpSender && RTCRtpSender.getCapabilities && RTCRtpSender.getCapabilities("video") &&
					RTCRtpSender.getCapabilities("video").codecs && RTCRtpSender.getCapabilities("video").codecs.length) {
				for(var codec of RTCRtpSender.getCapabilities("video").codecs) {
					if(codec && codec.mimeType && codec.mimeType.toLowerCase() === "video/vp8") {
						Janus.safariVp8 = true;
						break;
					}
				}
				if(Janus.safariVp8) {
					Janus.log("This version of Safari supports VP8");
				} else {
					Janus.warn("This version of Safari does NOT support VP8: if you're using a Technology Preview, " +
						"try enabling the 'WebRTC VP8 codec' setting in the 'Experimental Features' Develop menu");
				}
			} else {
				// We do it in a very ugly way, as there's no alternative...
				// We create a PeerConnection to see if VP8 is in an offer
				var testpc = new RTCPeerConnection({});
				testpc.createOffer({offerToReceiveVideo: true}).then(function(offer) {
					Janus.safariVp8 = offer.sdp.indexOf("VP8") !== -1;
					if(Janus.safariVp8) {
						Janus.log("This version of Safari supports VP8");
					} else {
						Janus.warn("This version of Safari does NOT support VP8: if you're using a Technology Preview, " +
							"try enabling the 'WebRTC VP8 codec' setting in the 'Experimental Features' Develop menu");
					}
					testpc.close();
					testpc = null;
				});
			}
		}
		// Check if this browser supports Unified Plan and transceivers
		// Based on https://codepen.io/anon/pen/ZqLwWV?editors=0010
		Janus.unifiedPlan = false;
		if(Janus.webRTCAdapter.browserDetails.browser === 'firefox' &&
				Janus.webRTCAdapter.browserDetails.version >= 59) {
			// Firefox definitely does, starting from version 59
			Janus.unifiedPlan = true;
		} else if(Janus.webRTCAdapter.browserDetails.browser === 'chrome' &&
				Janus.webRTCAdapter.browserDetails.version >= 72) {
			// Chrome does, but it's only usable from version 72 on
			Janus.unifiedPlan = true;
		} else if(!window.RTCRtpTransceiver || !('currentDirection' in RTCRtpTransceiver.prototype)) {
			// Safari supports addTransceiver() but not Unified Plan when
			// currentDirection is not defined (see codepen above).
			Janus.unifiedPlan = false;
		} else {
			// Check if addTransceiver() throws an exception
			var tempPc = new RTCPeerConnection();
			try {
				tempPc.addTransceiver('audio');
				Janus.unifiedPlan = true;
			} catch (e) {}
			tempPc.close();
		}
		Janus.initDone = true;
		options.callback();
	}
};

// Helper method to check whether WebRTC is supported by this browser
Janus.isWebrtcSupported = function() {
	return !!window.RTCPeerConnection;
};
// Helper method to check whether devices can be accessed by this browser (e.g., not possible via plain HTTP)
Janus.isGetUserMediaAvailable = function() {
	return navigator.mediaDevices && navigator.mediaDevices.getUserMedia;
};

// Helper method to create random identifiers (e.g., transaction)
Janus.randomString = function(len) {
	var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var randomString = '';
	for (var i = 0; i < len; i++) {
		var randomPoz = Math.floor(Math.random() * charSet.length);
		randomString += charSet.substring(randomPoz,randomPoz+1);
	}
	return randomString;
};

function Janus(gatewayCallbacks) {
	gatewayCallbacks = gatewayCallbacks || {};
	gatewayCallbacks.success = (typeof gatewayCallbacks.success == "function") ? gatewayCallbacks.success : Janus.noop;
	gatewayCallbacks.error = (typeof gatewayCallbacks.error == "function") ? gatewayCallbacks.error : Janus.noop;
	gatewayCallbacks.destroyed = (typeof gatewayCallbacks.destroyed == "function") ? gatewayCallbacks.destroyed : Janus.noop;
	if(!Janus.initDone) {
		gatewayCallbacks.error("Library not initialized");
		return {};
	}
	if(!Janus.isWebrtcSupported()) {
		gatewayCallbacks.error("WebRTC not supported by this browser");
		return {};
	}
	Janus.log("Library initialized: " + Janus.initDone);
	if(!gatewayCallbacks.server) {
		gatewayCallbacks.error("Invalid server url");
		return {};
	}
	var websockets = false;
	var ws = null;
	var wsHandlers = {};
	var wsKeepaliveTimeoutId = null;
	var servers = null;
	var serversIndex = 0;
	var server = gatewayCallbacks.server;
	if(Janus.isArray(server)) {
		Janus.log("Multiple servers provided (" + server.length + "), will use the first that works");
		server = null;
		servers = gatewayCallbacks.server;
		Janus.debug(servers);
	} else {
		if(server.indexOf("ws") === 0) {
			websockets = true;
			Janus.log("Using WebSockets to contact Janus: " + server);
		} else {
			websockets = false;
			Janus.log("Using REST API to contact Janus: " + server);
		}
	}
	var iceServers = gatewayCallbacks.iceServers || [{urls: "stun:stun.l.google.com:19302"}];
	var iceTransportPolicy = gatewayCallbacks.iceTransportPolicy;
	var bundlePolicy = gatewayCallbacks.bundlePolicy;
	// Whether IPv6 candidates should be gathered
	var ipv6Support = (gatewayCallbacks.ipv6 === true);
	// Whether we should enable the withCredentials flag for XHR requests
	var withCredentials = false;
	if(gatewayCallbacks.withCredentials !== undefined && gatewayCallbacks.withCredentials !== null)
		withCredentials = gatewayCallbacks.withCredentials === true;
	// Optional max events
	var maxev = 10;
	if(gatewayCallbacks.max_poll_events !== undefined && gatewayCallbacks.max_poll_events !== null)
		maxev = gatewayCallbacks.max_poll_events;
	if(maxev < 1)
		maxev = 1;
	// Token to use (only if the token based authentication mechanism is enabled)
	var token = null;
	if(gatewayCallbacks.token !== undefined && gatewayCallbacks.token !== null)
		token = gatewayCallbacks.token;
	// API secret to use (only if the shared API secret is enabled)
	var apisecret = null;
	if(gatewayCallbacks.apisecret !== undefined && gatewayCallbacks.apisecret !== null)
		apisecret = gatewayCallbacks.apisecret;
	// Whether we should destroy this session when onbeforeunload is called
	this.destroyOnUnload = true;
	if(gatewayCallbacks.destroyOnUnload !== undefined && gatewayCallbacks.destroyOnUnload !== null)
		this.destroyOnUnload = (gatewayCallbacks.destroyOnUnload === true);
	// Some timeout-related values
	var keepAlivePeriod = 25000;
	if(gatewayCallbacks.keepAlivePeriod !== undefined && gatewayCallbacks.keepAlivePeriod !== null)
		keepAlivePeriod = gatewayCallbacks.keepAlivePeriod;
	if(isNaN(keepAlivePeriod))
		keepAlivePeriod = 25000;
	var longPollTimeout = 60000;
	if(gatewayCallbacks.longPollTimeout !== undefined && gatewayCallbacks.longPollTimeout !== null)
		longPollTimeout = gatewayCallbacks.longPollTimeout;
	if(isNaN(longPollTimeout))
		longPollTimeout = 60000;

	// overrides for default maxBitrate values for simulcasting
	function getMaxBitrates(simulcastMaxBitrates) {
		var maxBitrates = {
			high: 900000,
			medium: 300000,
			low: 100000,
		};

		if (simulcastMaxBitrates !== undefined && simulcastMaxBitrates !== null) {
			if (simulcastMaxBitrates.high)
				maxBitrates.high = simulcastMaxBitrates.high;
			if (simulcastMaxBitrates.medium)
				maxBitrates.medium = simulcastMaxBitrates.medium;
			if (simulcastMaxBitrates.low)
				maxBitrates.low = simulcastMaxBitrates.low;
		}

		return maxBitrates;
	}

	var connected = false;
	var sessionId = null;
	var pluginHandles = {};
	var that = this;
	var retries = 0;
	var transactions = {};
	createSession(gatewayCallbacks);

	// Public methods
	this.getServer = function() { return server; };
	this.isConnected = function() { return connected; };
	this.reconnect = function(callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		callbacks["reconnect"] = true;
		createSession(callbacks);
	};
	this.getSessionId = function() { return sessionId; };
	this.getInfo = function(callbacks) { getInfo(callbacks); };
	this.destroy = function(callbacks) { destroySession(callbacks); };
	this.attach = function(callbacks) { createHandle(callbacks); };

	function eventHandler() {
		if(sessionId == null)
			return;
		Janus.debug('Long poll...');
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			return;
		}
		var longpoll = server + "/" + sessionId + "?rid=" + new Date().getTime();
		if(maxev)
			longpoll = longpoll + "&maxev=" + maxev;
		if(token)
			longpoll = longpoll + "&token=" + encodeURIComponent(token);
		if(apisecret)
			longpoll = longpoll + "&apisecret=" + encodeURIComponent(apisecret);
		Janus.httpAPICall(longpoll, {
			verb: 'GET',
			withCredentials: withCredentials,
			success: handleEvent,
			timeout: longPollTimeout,
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);
				retries++;
				if(retries > 3) {
					// Did we just lose the server? :-(
					connected = false;
					gatewayCallbacks.error("Lost connection to the server (is it down?)");
					return;
				}
				eventHandler();
			}
		});
	}

	// Private event handler: this will trigger plugin callbacks, if set
	function handleEvent(json, skipTimeout) {
		retries = 0;
		if(!websockets && sessionId !== undefined && sessionId !== null && skipTimeout !== true)
			eventHandler();
		if(!websockets && Janus.isArray(json)) {
			// We got an array: it means we passed a maxev > 1, iterate on all objects
			for(var i=0; i<json.length; i++) {
				handleEvent(json[i], true);
			}
			return;
		}
		if(json["janus"] === "keepalive") {
			// Nothing happened
			Janus.vdebug("Got a keepalive on session " + sessionId);
			return;
		} else if(json["janus"] === "server_info") {
			// Just info on the Janus instance
			Janus.debug("Got info on the Janus instance");
			Janus.debug(json);
			var transaction = json["transaction"];
			if(transaction) {
				var reportSuccess = transactions[transaction];
				if(reportSuccess)
					reportSuccess(json);
				delete transactions[transaction];
			}
			return;
		} else if(json["janus"] === "ack") {
			// Just an ack, we can probably ignore
			Janus.debug("Got an ack on session " + sessionId);
			Janus.debug(json);
			var transaction = json["transaction"];
			if(transaction) {
				var reportSuccess = transactions[transaction];
				if(reportSuccess)
					reportSuccess(json);
				delete transactions[transaction];
			}
			return;
		} else if(json["janus"] === "success") {
			// Success!
			Janus.debug("Got a success on session " + sessionId);
			Janus.debug(json);
			var transaction = json["transaction"];
			if(transaction) {
				var reportSuccess = transactions[transaction];
				if(reportSuccess)
					reportSuccess(json);
				delete transactions[transaction];
			}
			return;
		} else if(json["janus"] === "trickle") {
			// We got a trickle candidate from Janus
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.debug("This handle is not attached to this session");
				return;
			}
			var candidate = json["candidate"];
			Janus.debug("Got a trickled candidate on session " + sessionId);
			Janus.debug(candidate);
			var config = pluginHandle.webrtcStuff;
			if(config.pc && config.remoteSdp) {
				// Add candidate right now
				Janus.debug("Adding remote candidate:", candidate);
				if(!candidate || candidate.completed === true) {
					// end-of-candidates
					config.pc.addIceCandidate(Janus.endOfCandidates);
				} else {
					// New candidate
					config.pc.addIceCandidate(candidate);
				}
			} else {
				// We didn't do setRemoteDescription (trickle got here before the offer?)
				Janus.debug("We didn't do setRemoteDescription (trickle got here before the offer?), caching candidate");
				if(!config.candidates)
					config.candidates = [];
				config.candidates.push(candidate);
				Janus.debug(config.candidates);
			}
		} else if(json["janus"] === "webrtcup") {
			// The PeerConnection with the server is up! Notify this
			Janus.debug("Got a webrtcup event on session " + sessionId);
			Janus.debug(json);
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.debug("This handle is not attached to this session");
				return;
			}
			pluginHandle.webrtcState(true);
			return;
		} else if(json["janus"] === "hangup") {
			// A plugin asked the core to hangup a PeerConnection on one of our handles
			Janus.debug("Got a hangup event on session " + sessionId);
			Janus.debug(json);
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.debug("This handle is not attached to this session");
				return;
			}
			pluginHandle.webrtcState(false, json["reason"]);
			pluginHandle.hangup();
		} else if(json["janus"] === "detached") {
			// A plugin asked the core to detach one of our handles
			Janus.debug("Got a detached event on session " + sessionId);
			Janus.debug(json);
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				// Don't warn here because destroyHandle causes this situation.
				return;
			}
			pluginHandle.detached = true;
			pluginHandle.ondetached();
			pluginHandle.detach();
		} else if(json["janus"] === "media") {
			// Media started/stopped flowing
			Janus.debug("Got a media event on session " + sessionId);
			Janus.debug(json);
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.debug("This handle is not attached to this session");
				return;
			}
			pluginHandle.mediaState(json["type"], json["receiving"]);
		} else if(json["janus"] === "slowlink") {
			Janus.debug("Got a slowlink event on session " + sessionId);
			Janus.debug(json);
			// Trouble uplink or downlink
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.debug("This handle is not attached to this session");
				return;
			}
			pluginHandle.slowLink(json["uplink"], json["lost"]);
		} else if(json["janus"] === "error") {
			// Oops, something wrong happened
			Janus.error(1)
			Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
			Janus.debug(json);
			var transaction = json["transaction"];
			if(transaction) {
				var reportSuccess = transactions[transaction];
				if(reportSuccess) {
					reportSuccess(json);
				}
				delete transactions[transaction];
			}
			return;
		} else if(json["janus"] === "event") {
			Janus.debug("Got a plugin event on session " + sessionId);
			Janus.debug(json);
			var sender = json["sender"];
			if(!sender) {
				Janus.warn("Missing sender...");
				return;
			}
			var plugindata = json["plugindata"];
			if(!plugindata) {
				Janus.warn("Missing plugindata...");
				return;
			}
			Janus.debug("  -- Event is coming from " + sender + " (" + plugindata["plugin"] + ")");
			var data = plugindata["data"];
			Janus.debug(data);
			var pluginHandle = pluginHandles[sender];
			if(!pluginHandle) {
				Janus.warn("This handle is not attached to this session");
				return;
			}
			var jsep = json["jsep"];
			if(jsep) {
				Janus.debug("Handling SDP as well...");
				Janus.debug(jsep);
			}
			var callback = pluginHandle.onmessage;
			if(callback) {
				Janus.debug("Notifying application...");
				// Send to callback specified when attaching plugin handle
				callback(data, jsep);
			} else {
				// Send to generic callback (?)
				Janus.debug("No provided notification callback");
			}
		} else if(json["janus"] === "timeout") {
			Janus.error("Timeout on session " + sessionId);
			Janus.debug(json);
			if (websockets) {
				ws.close(3504, "Gateway timeout");
			}
			return;
		} else {
			Janus.warn("Unknown message/event  '" + json["janus"] + "' on session " + sessionId);
			Janus.debug(json);
		}
	}

	// Private helper to send keep-alive messages on WebSockets
	function keepAlive() {
		if(!server || !websockets || !connected)
			return;
		wsKeepaliveTimeoutId = setTimeout(keepAlive, keepAlivePeriod);
		var request = { "janus": "keepalive", "session_id": sessionId, "transaction": Janus.randomString(12) };
		if(token)
			request["token"] = token;
		if(apisecret)
			request["apisecret"] = apisecret;
		ws.send(JSON.stringify(request));
	}

	// Private method to create a session
	function createSession(callbacks) {
		var transaction = Janus.randomString(12);
		var request = { "janus": "create", "transaction": transaction };
		if(callbacks["reconnect"]) {
			// We're reconnecting, claim the session
			connected = false;
			request["janus"] = "claim";
			request["session_id"] = sessionId;
			// If we were using websockets, ignore the old connection
			if(ws) {
				ws.onopen = null;
				ws.onerror = null;
				ws.onclose = null;
				if(wsKeepaliveTimeoutId) {
					clearTimeout(wsKeepaliveTimeoutId);
					wsKeepaliveTimeoutId = null;
				}
			}
		}
		if(token)
			request["token"] = token;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(!server && Janus.isArray(servers)) {
			// We still need to find a working server from the list we were given
			server = servers[serversIndex];
			if(server.indexOf("ws") === 0) {
				websockets = true;
				Janus.log("Server #" + (serversIndex+1) + ": trying WebSockets to contact Janus (" + server + ")");
			} else {
				websockets = false;
				Janus.log("Server #" + (serversIndex+1) + ": trying REST API to contact Janus (" + server + ")");
			}
		}
		if(websockets) {
			ws = Janus.newWebSocket(server, 'janus-protocol');
			wsHandlers = {
				'error': function() {
					Janus.error("Error connecting to the Janus WebSockets server... " + server);
					if (Janus.isArray(servers) && !callbacks["reconnect"]) {
						serversIndex++;
						if (serversIndex === servers.length) {
							// We tried all the servers the user gave us and they all failed
							callbacks.error("Error connecting to any of the provided Janus servers: Is the server down?");
							return;
						}
						// Let's try the next server
						server = null;
						setTimeout(function() {
							createSession(callbacks);
						}, 200);
						return;
					}
					callbacks.error("Error connecting to the Janus WebSockets server: Is the server down?");
				},

				'open': function() {
					// We need to be notified about the success
					transactions[transaction] = function(json) {
						Janus.debug(json);
						if (json["janus"] !== "success") {
							Janus.error(2)
							Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
							callbacks.error(json["error"].reason);
							return;
						}
						wsKeepaliveTimeoutId = setTimeout(keepAlive, keepAlivePeriod);
						connected = true;
						sessionId = json["session_id"] ? json["session_id"] : json.data["id"];
						if(callbacks["reconnect"]) {
							Janus.log("Claimed session: " + sessionId);
						} else {
							Janus.log("Created session: " + sessionId);
						}
						Janus.sessions[sessionId] = that;
						callbacks.success();
					};
					ws.send(JSON.stringify(request));
				},

				'message': function(event) {
					handleEvent(JSON.parse(event.data));
				},

				'close': function() {
					if (!server || !connected) {
						return;
					}
					connected = false;
					// FIXME What if this is called when the page is closed?
					gatewayCallbacks.error("Lost connection to the server (is it down?)");
				}
			};

			for(var eventName in wsHandlers) {
				ws.addEventListener(eventName, wsHandlers[eventName]);
			}

			return;
		}
		Janus.httpAPICall(server, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.debug(json);
				if(json["janus"] !== "success") {
					Janus.error(3)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
					callbacks.error(json["error"].reason);
					return;
				}
				connected = true;
				sessionId = json["session_id"] ? json["session_id"] : json.data["id"];
				if(callbacks["reconnect"]) {
					Janus.log("Claimed session: " + sessionId);
				} else {
					Janus.log("Created session: " + sessionId);
				}
				Janus.sessions[sessionId] = that;
				eventHandler();
				callbacks.success();
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				if(Janus.isArray(servers) && !callbacks["reconnect"]) {
					serversIndex++;
					if(serversIndex === servers.length) {
						// We tried all the servers the user gave us and they all failed
						callbacks.error("Error connecting to any of the provided Janus servers: Is the server down?");
						return;
					}
					// Let's try the next server
					server = null;
					setTimeout(function() { createSession(callbacks); }, 200);
					return;
				}
				if(errorThrown === "")
					callbacks.error(textStatus + ": Is the server down?");
				else
					callbacks.error(textStatus + ": " + errorThrown);
			}
		});
	}

	// Private method to get info on the server
	function getInfo(callbacks) {
		callbacks = callbacks || {};
		// FIXME This method triggers a success even when we fail
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		Janus.log("Getting info on Janus instance");
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			callbacks.error("Is the server down? (connected=false)");
			return;
		}
		// We just need to send an "info" request
		var transaction = Janus.randomString(12);
		var request = { "janus": "info", "transaction": transaction };
		if(token)
			request["token"] = token;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(websockets) {
			transactions[transaction] = function(json) {
				Janus.log("Server info:");
				Janus.debug(json);
				if(json["janus"] !== "server_info") {
					Janus.error(4)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
				}
				callbacks.success(json);
			}
			ws.send(JSON.stringify(request));
			return;
		}
		Janus.httpAPICall(server, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.log("Server info:");
				Janus.debug(json);
				if(json["janus"] !== "server_info") {
					Janus.error(5)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
				}
				callbacks.success(json);
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				if(errorThrown === "")
					callbacks.error(textStatus + ": Is the server down?");
				else
					callbacks.error(textStatus + ": " + errorThrown);
			}
		});
	}

	// Private method to destroy a session
	function destroySession(callbacks) {
		callbacks = callbacks || {};
		// FIXME This method triggers a success even when we fail
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		var unload = (callbacks.unload === true);
		var notifyDestroyed = true;
		if(callbacks.notifyDestroyed !== undefined && callbacks.notifyDestroyed !== null)
			notifyDestroyed = (callbacks.notifyDestroyed === true);
		var cleanupHandles = (callbacks.cleanupHandles === true);
		Janus.log("Destroying session " + sessionId + " (unload=" + unload + ")");
		if(!sessionId) {
			Janus.warn("No session to destroy");
			callbacks.success();
			if(notifyDestroyed)
				gatewayCallbacks.destroyed();
			return;
		}
		if(cleanupHandles) {
			for(var handleId in pluginHandles)
				destroyHandle(handleId, { noRequest: true });
		}
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			sessionId = null;
			callbacks.success();
			return;
		}
		// No need to destroy all handles first, Janus will do that itself
		var request = { "janus": "destroy", "transaction": Janus.randomString(12) };
		if(token)
			request["token"] = token;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(unload) {
			// We're unloading the page: use sendBeacon for HTTP instead,
			// or just close the WebSocket connection if we're using that
			if(websockets) {
				ws.onclose = null;
				ws.close();
				ws = null;
			} else {
				navigator.sendBeacon(server + "/" + sessionId, JSON.stringify(request));
			}
			Janus.log("Destroyed session:");
			sessionId = null;
			connected = false;
			callbacks.success();
			if(notifyDestroyed)
				gatewayCallbacks.destroyed();
			return;
		}
		if(websockets) {
			request["session_id"] = sessionId;

			var unbindWebSocket = function() {
				for(var eventName in wsHandlers) {
					ws.removeEventListener(eventName, wsHandlers[eventName]);
				}
				ws.removeEventListener('message', onUnbindMessage);
				ws.removeEventListener('error', onUnbindError);
				if(wsKeepaliveTimeoutId) {
					clearTimeout(wsKeepaliveTimeoutId);
				}
				ws.close();
			};

			var onUnbindMessage = function(event){
				var data = JSON.parse(event.data);
				if(data.session_id == request.session_id && data.transaction == request.transaction) {
					unbindWebSocket();
					callbacks.success();
					if(notifyDestroyed)
						gatewayCallbacks.destroyed();
				}
			};
			var onUnbindError = function(event) {
				unbindWebSocket();
				callbacks.error("Failed to destroy the server: Is the server down?");
				if(notifyDestroyed)
					gatewayCallbacks.destroyed();
			};

			ws.addEventListener('message', onUnbindMessage);
			ws.addEventListener('error', onUnbindError);

			if (ws.readyState === 1) {
				ws.send(JSON.stringify(request));
			} else {
				onUnbindError();
			}

			return;
		}
		Janus.httpAPICall(server + "/" + sessionId, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.log("Destroyed session:");
				Janus.debug(json);
				sessionId = null;
				connected = false;
				if(json["janus"] !== "success") {
					Janus.error(6)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
				}
				callbacks.success();
				if(notifyDestroyed)
					gatewayCallbacks.destroyed();
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				// Reset everything anyway
				sessionId = null;
				connected = false;
				callbacks.success();
				if(notifyDestroyed)
					gatewayCallbacks.destroyed();
			}
		});
	}

	// Private method to create a plugin handle
	function createHandle(callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		callbacks.consentDialog = (typeof callbacks.consentDialog == "function") ? callbacks.consentDialog : Janus.noop;
		callbacks.iceState = (typeof callbacks.iceState == "function") ? callbacks.iceState : Janus.noop;
		callbacks.mediaState = (typeof callbacks.mediaState == "function") ? callbacks.mediaState : Janus.noop;
		callbacks.webrtcState = (typeof callbacks.webrtcState == "function") ? callbacks.webrtcState : Janus.noop;
		callbacks.slowLink = (typeof callbacks.slowLink == "function") ? callbacks.slowLink : Janus.noop;
		callbacks.onmessage = (typeof callbacks.onmessage == "function") ? callbacks.onmessage : Janus.noop;
		callbacks.onlocalstream = (typeof callbacks.onlocalstream == "function") ? callbacks.onlocalstream : Janus.noop;
		callbacks.onremotestream = (typeof callbacks.onremotestream == "function") ? callbacks.onremotestream : Janus.noop;
		callbacks.ondata = (typeof callbacks.ondata == "function") ? callbacks.ondata : Janus.noop;
		callbacks.ondataopen = (typeof callbacks.ondataopen == "function") ? callbacks.ondataopen : Janus.noop;
		callbacks.oncleanup = (typeof callbacks.oncleanup == "function") ? callbacks.oncleanup : Janus.noop;
		callbacks.ondetached = (typeof callbacks.ondetached == "function") ? callbacks.ondetached : Janus.noop;
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			callbacks.error("Is the server down? (connected=false)");
			return;
		}
		var plugin = callbacks.plugin;
		if(!plugin) {
			Janus.error("Invalid plugin");
			callbacks.error("Invalid plugin");
			return;
		}
		var opaqueId = callbacks.opaqueId;
		var handleToken = callbacks.token ? callbacks.token : token;
		var transaction = Janus.randomString(12);
		var request = { "janus": "attach", "plugin": plugin, "opaque_id": opaqueId, "transaction": transaction };
		if(handleToken)
			request["token"] = handleToken;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(websockets) {
			transactions[transaction] = function(json) {
				Janus.debug(json);
				if(json["janus"] !== "success") {
			Janus.error(7)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
					callbacks.error("Ooops: " + json["error"].code + " " + json["error"].reason);
					return;
				}
				var handleId = json.data["id"];
				Janus.log("Created handle: " + handleId);
				var pluginHandle =
					{
						session : that,
						plugin : plugin,
						id : handleId,
						token : handleToken,
						detached : false,
						webrtcStuff : {
							started : false,
							myStream : null,
							streamExternal : false,
							remoteStream : null,
							mySdp : null,
							mediaConstraints : null,
							pc : null,
							dataChannel : {},
							dtmfSender : null,
							trickle : true,
							iceDone : false,
							volume : {
								value : null,
								timer : null
							},
							bitrate : {
								value : null,
								bsnow : null,
								bsbefore : null,
								tsnow : null,
								tsbefore : null,
								timer : null
							}
						},
						getId : function() { return handleId; },
						getPlugin : function() { return plugin; },
						getVolume : function() { return getVolume(handleId, true); },
						getRemoteVolume : function() { return getVolume(handleId, true); },
						getLocalVolume : function() { return getVolume(handleId, false); },
						isAudioMuted : function() { return isMuted(handleId, false); },
						muteAudio : function() { return mute(handleId, false, true); },
						unmuteAudio : function() { return mute(handleId, false, false); },
						isVideoMuted : function() { return isMuted(handleId, true); },
						muteVideo : function() { return mute(handleId, true, true); },
						unmuteVideo : function() { return mute(handleId, true, false); },
						getBitrate : function() { return getBitrate(handleId); },
						send : function(callbacks) { sendMessage(handleId, callbacks); },
						data : function(callbacks) { sendData(handleId, callbacks); },
						dtmf : function(callbacks) { sendDtmf(handleId, callbacks); },
						consentDialog : callbacks.consentDialog,
						iceState : callbacks.iceState,
						mediaState : callbacks.mediaState,
						webrtcState : callbacks.webrtcState,
						slowLink : callbacks.slowLink,
						onmessage : callbacks.onmessage,
						createOffer : function(callbacks) { prepareWebrtc(handleId, true, callbacks); },
						createAnswer : function(callbacks) { prepareWebrtc(handleId, false, callbacks); },
						handleRemoteJsep : function(callbacks) { prepareWebrtcPeer(handleId, callbacks); },
						onlocalstream : callbacks.onlocalstream,
						onremotestream : callbacks.onremotestream,
						ondata : callbacks.ondata,
						ondataopen : callbacks.ondataopen,
						oncleanup : callbacks.oncleanup,
						ondetached : callbacks.ondetached,
						hangup : function(sendRequest) { cleanupWebrtc(handleId, sendRequest === true); },
						detach : function(callbacks) { destroyHandle(handleId, callbacks); }
					};
				pluginHandles[handleId] = pluginHandle;
				callbacks.success(pluginHandle);
			};
			request["session_id"] = sessionId;
			ws.send(JSON.stringify(request));
			return;
		}
		Janus.httpAPICall(server + "/" + sessionId, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.debug(json);
				if(json["janus"] !== "success") {

			Janus.error(9)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
					callbacks.error("Ooops: " + json["error"].code + " " + json["error"].reason);
					return;
				}
				var handleId = json.data["id"];
				Janus.log("Created handle: " + handleId);
				var pluginHandle =
					{
						session : that,
						plugin : plugin,
						id : handleId,
						token : handleToken,
						detached : false,
						webrtcStuff : {
							started : false,
							myStream : null,
							streamExternal : false,
							remoteStream : null,
							mySdp : null,
							mediaConstraints : null,
							pc : null,
							dataChannel : {},
							dtmfSender : null,
							trickle : true,
							iceDone : false,
							volume : {
								value : null,
								timer : null
							},
							bitrate : {
								value : null,
								bsnow : null,
								bsbefore : null,
								tsnow : null,
								tsbefore : null,
								timer : null
							}
						},
						getId : function() { return handleId; },
						getPlugin : function() { return plugin; },
						getVolume : function() { return getVolume(handleId, true); },
						getRemoteVolume : function() { return getVolume(handleId, true); },
						getLocalVolume : function() { return getVolume(handleId, false); },
						isAudioMuted : function() { return isMuted(handleId, false); },
						muteAudio : function() { return mute(handleId, false, true); },
						unmuteAudio : function() { return mute(handleId, false, false); },
						isVideoMuted : function() { return isMuted(handleId, true); },
						muteVideo : function() { return mute(handleId, true, true); },
						unmuteVideo : function() { return mute(handleId, true, false); },
						getBitrate : function() { return getBitrate(handleId); },
						send : function(callbacks) { sendMessage(handleId, callbacks); },
						data : function(callbacks) { sendData(handleId, callbacks); },
						dtmf : function(callbacks) { sendDtmf(handleId, callbacks); },
						consentDialog : callbacks.consentDialog,
						iceState : callbacks.iceState,
						mediaState : callbacks.mediaState,
						webrtcState : callbacks.webrtcState,
						slowLink : callbacks.slowLink,
						onmessage : callbacks.onmessage,
						createOffer : function(callbacks) { prepareWebrtc(handleId, true, callbacks); },
						createAnswer : function(callbacks) { prepareWebrtc(handleId, false, callbacks); },
						handleRemoteJsep : function(callbacks) { prepareWebrtcPeer(handleId, callbacks); },
						onlocalstream : callbacks.onlocalstream,
						onremotestream : callbacks.onremotestream,
						ondata : callbacks.ondata,
						ondataopen : callbacks.ondataopen,
						oncleanup : callbacks.oncleanup,
						ondetached : callbacks.ondetached,
						hangup : function(sendRequest) { cleanupWebrtc(handleId, sendRequest === true); },
						detach : function(callbacks) { destroyHandle(handleId, callbacks); }
					}
				pluginHandles[handleId] = pluginHandle;
				callbacks.success(pluginHandle);
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				if(errorThrown === "")
					callbacks.error(textStatus + ": Is the server down?");
				else
					callbacks.error(textStatus + ": " + errorThrown);
			}
		});
	}

	// Private method to send a message
	function sendMessage(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			callbacks.error("Is the server down? (connected=false)");
			return;
		}
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var message = callbacks.message;
		var jsep = callbacks.jsep;
		var transaction = Janus.randomString(12);
		var request = { "janus": "message", "body": message, "transaction": transaction };
		if(pluginHandle.token)
			request["token"] = pluginHandle.token;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(jsep) {
			request.jsep = {
				type: jsep.type,
				sdp: jsep.sdp
			};
			if(jsep.e2ee)
				request.jsep.e2ee = true;
			if(jsep.rid_order === "hml" || jsep.rid_order === "lmh")
				request.jsep.rid_order = jsep.rid_order;
		}
		Janus.debug("Sending message to plugin (handle=" + handleId + "):");
		Janus.debug(request);
		if(websockets) {
			request["session_id"] = sessionId;
			request["handle_id"] = handleId;
			transactions[transaction] = function(json) {
				Janus.debug("Message sent!");
				Janus.debug(json);
				if(json["janus"] === "success") {
					// We got a success, must have been a synchronous transaction
					var plugindata = json["plugindata"];
					if(!plugindata) {
						Janus.warn("Request succeeded, but missing plugindata...");
						callbacks.success();
						return;
					}
					Janus.log("Synchronous transaction successful (" + plugindata["plugin"] + ")");
					var data = plugindata["data"];
					Janus.debug(data);
					callbacks.success(data);
					return;
				} else if(json["janus"] !== "ack") {
					// Not a success and not an ack, must be an error
					if(json["error"]) {

			Janus.error(11)
						Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
						callbacks.error(json["error"].code + " " + json["error"].reason);
					} else {
						Janus.error("Unknown error");	// FIXME
						callbacks.error("Unknown error");
					}
					return;
				}
				// If we got here, the plugin decided to handle the request asynchronously
				callbacks.success();
			};
			ws.send(JSON.stringify(request));
			return;
		}
		Janus.httpAPICall(server + "/" + sessionId + "/" + handleId, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.debug("Message sent!");
				Janus.debug(json);
				if(json["janus"] === "success") {
					// We got a success, must have been a synchronous transaction
					var plugindata = json["plugindata"];
					if(!plugindata) {
						Janus.warn("Request succeeded, but missing plugindata...");
						callbacks.success();
						return;
					}
					Janus.log("Synchronous transaction successful (" + plugindata["plugin"] + ")");
					var data = plugindata["data"];
					Janus.debug(data);
					callbacks.success(data);
					return;
				} else if(json["janus"] !== "ack") {
					// Not a success and not an ack, must be an error
					if(json["error"]) {
						console.log(request)
						Janus.error(12)
						Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
						callbacks.error(json["error"].code + " " + json["error"].reason);
					} else {
						Janus.error("Unknown error");	// FIXME
						callbacks.error("Unknown error");
					}
					return;
				}
				// If we got here, the plugin decided to handle the request asynchronously
				callbacks.success();
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				callbacks.error(textStatus + ": " + errorThrown);
			}
		});
	}

	// Private method to send a trickle candidate
	function sendTrickleCandidate(handleId, candidate) {
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			return;
		}
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return;
		}
		var request = { "janus": "trickle", "candidate": candidate, "transaction": Janus.randomString(12) };
		if(pluginHandle.token)
			request["token"] = pluginHandle.token;
		if(apisecret)
			request["apisecret"] = apisecret;
		Janus.vdebug("Sending trickle candidate (handle=" + handleId + "):");
		Janus.vdebug(request);
		if(websockets) {
			request["session_id"] = sessionId;
			request["handle_id"] = handleId;
			ws.send(JSON.stringify(request));
			return;
		}
		Janus.httpAPICall(server + "/" + sessionId + "/" + handleId, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.vdebug("Candidate sent!");
				Janus.vdebug(json);
				if(json["janus"] !== "ack") {

			Janus.error(13)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
					return;
				}
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
			}
		});
	}

	// Private method to create a data channel
	function createDataChannel(handleId, dclabel, dcprotocol, incoming, pendingData) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		if(!config.pc) {
			Janus.warn("Invalid PeerConnection");
			return;
		}
		var onDataChannelMessage = function(event) {
			Janus.log('Received message on data channel:', event);
			var label = event.target.label;
			pluginHandle.ondata(event.data, label);
		};
		var onDataChannelStateChange = function(event) {
			Janus.log('Received state change on data channel:', event);
			var label = event.target.label;
			var protocol = event.target.protocol;
			var dcState = config.dataChannel[label] ? config.dataChannel[label].readyState : "null";
			Janus.log('State change on <' + label + '> data channel: ' + dcState);
			if(dcState === 'open') {
				// Any pending messages to send?
				if(config.dataChannel[label].pending && config.dataChannel[label].pending.length > 0) {
					Janus.log("Sending pending messages on <" + label + ">:", config.dataChannel[label].pending.length);
					for(var data of config.dataChannel[label].pending) {
						Janus.log("Sending data on data channel <" + label + ">");
						Janus.debug(data);
						config.dataChannel[label].send(data);
					}
					config.dataChannel[label].pending = [];
				}
				// Notify the open data channel
				pluginHandle.ondataopen(label, protocol);
			}
		};
		var onDataChannelError = function(error) {
			Janus.error('Got error on data channel:', error);
			// TODO
		};
		if(!incoming) {
			// FIXME Add options (ordered, maxRetransmits, etc.)
			var dcoptions = { ordered: true };
			if(dcprotocol)
				dcoptions.protocol = dcprotocol;
			config.dataChannel[dclabel] = config.pc.createDataChannel(dclabel, dcoptions);
		} else {
			// The channel was created by Janus
			config.dataChannel[dclabel] = incoming;
		}
		config.dataChannel[dclabel].onmessage = onDataChannelMessage;
		config.dataChannel[dclabel].onopen = onDataChannelStateChange;
		config.dataChannel[dclabel].onclose = onDataChannelStateChange;
		config.dataChannel[dclabel].onerror = onDataChannelError;
		config.dataChannel[dclabel].pending = [];
		if(pendingData)
			config.dataChannel[dclabel].pending.push(pendingData);
	}

	// Private method to send a data channel message
	function sendData(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		var data = callbacks.text || callbacks.data;
		if(!data) {
			Janus.warn("Invalid data");
			callbacks.error("Invalid data");
			return;
		}
		var label = callbacks.label ? callbacks.label : Janus.dataChanDefaultLabel;
		if(!config.dataChannel[label]) {
			// Create new data channel and wait for it to open
			createDataChannel(handleId, label, callbacks.protocol, false, data, callbacks.protocol);
			callbacks.success();
			return;
		}
		if(config.dataChannel[label].readyState !== "open") {
			config.dataChannel[label].pending.push(data);
			callbacks.success();
			return;
		}
		Janus.log("Sending data on data channel <" + label + ">");
		Janus.debug(data);
		config.dataChannel[label].send(data);
		callbacks.success();
	}

	// Private method to send a DTMF tone
	function sendDtmf(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		if(!config.dtmfSender) {
			// Create the DTMF sender the proper way, if possible
			if(config.pc) {
				var senders = config.pc.getSenders();
				var audioSender = senders.find(function(sender) {
					return sender.track && sender.track.kind === 'audio';
				});
				if(!audioSender) {
					Janus.warn("Invalid DTMF configuration (no audio track)");
					callbacks.error("Invalid DTMF configuration (no audio track)");
					return;
				}
				config.dtmfSender = audioSender.dtmf;
				if(config.dtmfSender) {
					Janus.log("Created DTMF Sender");
					config.dtmfSender.ontonechange = function(tone) { Janus.debug("Sent DTMF tone: " + tone.tone); };
				}
			}
			if(!config.dtmfSender) {
				Janus.warn("Invalid DTMF configuration");
				callbacks.error("Invalid DTMF configuration");
				return;
			}
		}
		var dtmf = callbacks.dtmf;
		if(!dtmf) {
			Janus.warn("Invalid DTMF parameters");
			callbacks.error("Invalid DTMF parameters");
			return;
		}
		var tones = dtmf.tones;
		if(!tones) {
			Janus.warn("Invalid DTMF string");
			callbacks.error("Invalid DTMF string");
			return;
		}
		var duration = (typeof dtmf.duration === 'number') ? dtmf.duration : 500; // We choose 500ms as the default duration for a tone
		var gap = (typeof dtmf.gap === 'number') ? dtmf.gap : 50; // We choose 50ms as the default gap between tones
		Janus.debug("Sending DTMF string " + tones + " (duration " + duration + "ms, gap " + gap + "ms)");
		config.dtmfSender.insertDTMF(tones, duration, gap);
		callbacks.success();
	}

	// Private method to destroy a plugin handle
	function destroyHandle(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		var noRequest = (callbacks.noRequest === true);
		Janus.log("Destroying handle " + handleId + " (only-locally=" + noRequest + ")");
		cleanupWebrtc(handleId);
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || pluginHandle.detached) {
			// Plugin was already detached by Janus, calling detach again will return a handle not found error, so just exit here
			delete pluginHandles[handleId];
			callbacks.success();
			return;
		}
		if(noRequest) {
			// We're only removing the handle locally
			delete pluginHandles[handleId];
			callbacks.success();
			return;
		}
		if(!connected) {
			Janus.warn("Is the server down? (connected=false)");
			callbacks.error("Is the server down? (connected=false)");
			return;
		}
		var request = { "janus": "detach", "transaction": Janus.randomString(12) };
		if(pluginHandle.token)
			request["token"] = pluginHandle.token;
		if(apisecret)
			request["apisecret"] = apisecret;
		if(websockets) {
			request["session_id"] = sessionId;
			request["handle_id"] = handleId;
			ws.send(JSON.stringify(request));
			delete pluginHandles[handleId];
			callbacks.success();
			return;
		}
		Janus.httpAPICall(server + "/" + sessionId + "/" + handleId, {
			verb: 'POST',
			withCredentials: withCredentials,
			body: request,
			success: function(json) {
				Janus.log("Destroyed handle:");
				Janus.debug(json);
				if(json["janus"] !== "success") {
					Janus.error(14)
					Janus.error("Ooops: " + json["error"].code + " " + json["error"].reason);	// FIXME
				}
				delete pluginHandles[handleId];
				callbacks.success();
			},
			error: function(textStatus, errorThrown) {
				Janus.error(textStatus + ":", errorThrown);	// FIXME
				// We cleanup anyway
				delete pluginHandles[handleId];
				callbacks.success();
			}
		});
	}

	// WebRTC stuff
	function streamsDone(handleId, jsep, media, callbacks, stream) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			// Close all tracks if the given stream has been created internally
			if(!callbacks.stream) {
				Janus.stopAllTracks(stream);
			}
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		Janus.debug("streamsDone:", stream);
		if(stream) {
			Janus.debug("  -- Audio tracks:", stream.getAudioTracks());
			Janus.debug("  -- Video tracks:", stream.getVideoTracks());
		}
		// We're now capturing the new stream: check if we're updating or if it's a new thing
		var addTracks = false;
		if(!config.myStream || !media.update || config.streamExternal) {
			config.myStream = stream;
			addTracks = true;
		} else {
			// We only need to update the existing stream
			if(((!media.update && isAudioSendEnabled(media)) || (media.update && (media.addAudio || media.replaceAudio))) &&
					stream.getAudioTracks() && stream.getAudioTracks().length) {
				config.myStream.addTrack(stream.getAudioTracks()[0]);
				if(Janus.unifiedPlan) {
					// Use Transceivers
					Janus.log((media.replaceAudio ? "Replacing" : "Adding") + " audio track:", stream.getAudioTracks()[0]);
					var audioTransceiver = null;
					var transceivers = config.pc.getTransceivers();
					if(transceivers && transceivers.length > 0) {
						for(var t of transceivers) {
							if((t.sender && t.sender.track && t.sender.track.kind === "audio") ||
									(t.receiver && t.receiver.track && t.receiver.track.kind === "audio")) {
								audioTransceiver = t;
								break;
							}
						}
					}
					if(audioTransceiver && audioTransceiver.sender) {
						audioTransceiver.sender.replaceTrack(stream.getAudioTracks()[0]);
					} else {
						config.pc.addTrack(stream.getAudioTracks()[0], stream);
					}
				} else {
					Janus.log((media.replaceAudio ? "Replacing" : "Adding") + " audio track:", stream.getAudioTracks()[0]);
					config.pc.addTrack(stream.getAudioTracks()[0], stream);
				}
			}
			if(((!media.update && isVideoSendEnabled(media)) || (media.update && (media.addVideo || media.replaceVideo))) &&
					stream.getVideoTracks() && stream.getVideoTracks().length) {
				config.myStream.addTrack(stream.getVideoTracks()[0]);
				if(Janus.unifiedPlan) {
					// Use Transceivers
					Janus.log((media.replaceVideo ? "Replacing" : "Adding") + " video track:", stream.getVideoTracks()[0]);
					var videoTransceiver = null;
					var transceivers = config.pc.getTransceivers();
					if(transceivers && transceivers.length > 0) {
						for(var t of transceivers) {
							if((t.sender && t.sender.track && t.sender.track.kind === "video") ||
									(t.receiver && t.receiver.track && t.receiver.track.kind === "video")) {
								videoTransceiver = t;
								break;
							}
						}
					}
					if(videoTransceiver && videoTransceiver.sender) {
						videoTransceiver.sender.replaceTrack(stream.getVideoTracks()[0]);
					} else {
						config.pc.addTrack(stream.getVideoTracks()[0], stream);
					}
				} else {
					Janus.log((media.replaceVideo ? "Replacing" : "Adding") + " video track:", stream.getVideoTracks()[0]);
					config.pc.addTrack(stream.getVideoTracks()[0], stream);
				}
			}
		}
		// If we still need to create a PeerConnection, let's do that
		if(!config.pc) {
			var pc_config = {"iceServers": iceServers, "iceTransportPolicy": iceTransportPolicy, "bundlePolicy": bundlePolicy};
			if(Janus.webRTCAdapter.browserDetails.browser === "chrome") {
				// For Chrome versions before 72, we force a plan-b semantic, and unified-plan otherwise
				pc_config["sdpSemantics"] = (Janus.webRTCAdapter.browserDetails.version < 72) ? "plan-b" : "unified-plan";
			}
			var pc_constraints = {
				"optional": [{"DtlsSrtpKeyAgreement": true}]
			};
			if(ipv6Support) {
				pc_constraints.optional.push({"googIPv6":true});
			}
			// Any custom constraint to add?
			if(callbacks.rtcConstraints && typeof callbacks.rtcConstraints === 'object') {
				Janus.debug("Adding custom PeerConnection constraints:", callbacks.rtcConstraints);
				for(var i in callbacks.rtcConstraints) {
					pc_constraints.optional.push(callbacks.rtcConstraints[i]);
				}
			}
			if(Janus.webRTCAdapter.browserDetails.browser === "edge") {
				// This is Edge, enable BUNDLE explicitly
				pc_config.bundlePolicy = "max-bundle";
			}
			// Check if a sender or receiver transform has been provided
			if(RTCRtpSender && (RTCRtpSender.prototype.createEncodedStreams ||
					(RTCRtpSender.prototype.createEncodedAudioStreams &&
					RTCRtpSender.prototype.createEncodedVideoStreams)) &&
					(callbacks.senderTransforms || callbacks.receiverTransforms)) {
				config.senderTransforms = callbacks.senderTransforms;
				config.receiverTransforms = callbacks.receiverTransforms;
				pc_config["forceEncodedAudioInsertableStreams"] = true;
				pc_config["forceEncodedVideoInsertableStreams"] = true;
				pc_config["encodedInsertableStreams"] = true;
			}
			Janus.log("Creating PeerConnection");
			Janus.debug(pc_constraints);
			config.pc = new RTCPeerConnection(pc_config, pc_constraints);
			Janus.debug(config.pc);
			if(config.pc.getStats) {	// FIXME
				config.volume = {};
				config.bitrate.value = "0 kbits/sec";
			}
			Janus.log("Preparing local SDP and gathering candidates (trickle=" + config.trickle + ")");
			config.pc.oniceconnectionstatechange = function(e) {
				if(config.pc)
					pluginHandle.iceState(config.pc.iceConnectionState);
			};
			config.pc.onicecandidate = function(event) {
				if (!event.candidate ||
						(Janus.webRTCAdapter.browserDetails.browser === 'edge' && event.candidate.candidate.indexOf('endOfCandidates') > 0)) {
					Janus.log("End of candidates.");
					config.iceDone = true;
					if(config.trickle === true) {
						// Notify end of candidates
						sendTrickleCandidate(handleId, {"completed": true});
					} else {
						// No trickle, time to send the complete SDP (including all candidates)
						sendSDP(handleId, callbacks);
					}
				} else {
					// JSON.stringify doesn't work on some WebRTC objects anymore
					// See https://code.google.com/p/chromium/issues/detail?id=467366
					var candidate = {
						"candidate": event.candidate.candidate,
						"sdpMid": event.candidate.sdpMid,
						"sdpMLineIndex": event.candidate.sdpMLineIndex
					};
					if(config.trickle === true) {
						// Send candidate
						sendTrickleCandidate(handleId, candidate);
					}
				}
			};
			config.pc.ontrack = function(event) {
				Janus.log("Handling Remote Track");
				Janus.debug(event);
				if(!event.streams)
					return;
				config.remoteStream = event.streams[0];
				pluginHandle.onremotestream(config.remoteStream);
				if(event.track.onended)
					return;
				if(config.receiverTransforms) {
					var receiverStreams = null;
					if(RTCRtpSender.prototype.createEncodedStreams) {
						receiverStreams = event.receiver.createEncodedStreams();
					} else if(RTCRtpSender.prototype.createAudioEncodedStreams || RTCRtpSender.prototype.createEncodedVideoStreams) {
						if(event.track.kind === "audio" && config.receiverTransforms["audio"]) {
							receiverStreams = event.receiver.createEncodedAudioStreams();
						} else if(event.track.kind === "video" && config.receiverTransforms["video"]) {
							receiverStreams = event.receiver.createEncodedVideoStreams();
						}
					}
					if(receiverStreams) {
						console.log(receiverStreams);
						if(receiverStreams.readableStream && receiverStreams.writableStream) {
							receiverStreams.readableStream
								.pipeThrough(config.receiverTransforms[event.track.kind])
								.pipeTo(receiverStreams.writableStream);
						} else if(receiverStreams.readable && receiverStreams.writable) {
							receiverStreams.readable
								.pipeThrough(config.receiverTransforms[event.track.kind])
								.pipeTo(receiverStreams.writable);
						}
					}
				}
				var trackMutedTimeoutId = null;
				Janus.log("Adding onended callback to track:", event.track);
				event.track.onended = function(ev) {
					Janus.log("Remote track removed:", ev);
					if(config.remoteStream) {
						clearTimeout(trackMutedTimeoutId);
						config.remoteStream.removeTrack(ev.target);
						pluginHandle.onremotestream(config.remoteStream);
					}
				};
				event.track.onmute = function(ev) {
					Janus.log("Remote track muted:", ev);
					if(config.remoteStream && trackMutedTimeoutId == null) {
						trackMutedTimeoutId = setTimeout(function() {
							Janus.log("Removing remote track");
							if (config.remoteStream) {
								config.remoteStream.removeTrack(ev.target);
								pluginHandle.onremotestream(config.remoteStream);
							}
							trackMutedTimeoutId = null;
						// Chrome seems to raise mute events only at multiples of 834ms;
						// we set the timeout to three times this value (rounded to 840ms)
						}, 3 * 840);
					}
				};
				event.track.onunmute = function(ev) {
					Janus.log("Remote track flowing again:", ev);
					if(trackMutedTimeoutId != null) {
						clearTimeout(trackMutedTimeoutId);
						trackMutedTimeoutId = null;
					} else {
						try {
							config.remoteStream.addTrack(ev.target);
							pluginHandle.onremotestream(config.remoteStream);
						} catch(e) {
							Janus.error(e);
						};
					}
				};
			};
		}
		if(addTracks && stream) {
			Janus.log('Adding local stream');
			var simulcast2 = (callbacks.simulcast2 === true);
			stream.getTracks().forEach(function(track) {
				Janus.log('Adding local track:', track);
				var sender = null;
				if(!simulcast2 || track.kind === 'audio') {
					sender = config.pc.addTrack(track, stream);
				} else {
					Janus.log('Enabling rid-based simulcasting:', track);
					var maxBitrates = getMaxBitrates(callbacks.simulcastMaxBitrates);
					var tr = config.pc.addTransceiver(track, {
						direction: "sendrecv",
						streams: [stream],
						sendEncodings: callbacks.sendEncodings || [
							{ rid: "h", active: true, maxBitrate: maxBitrates.high },
							{ rid: "m", active: true, maxBitrate: maxBitrates.medium, scaleResolutionDownBy: 2 },
							{ rid: "l", active: true, maxBitrate: maxBitrates.low, scaleResolutionDownBy: 4 }
						]
					});
					if(tr)
						sender = tr.sender;
				}
				// Check if insertable streams are involved
				if(sender && config.senderTransforms) {
					var senderStreams = null;
					if(RTCRtpSender.prototype.createEncodedStreams) {
						senderStreams = sender.createEncodedStreams();
					} else if(RTCRtpSender.prototype.createAudioEncodedStreams || RTCRtpSender.prototype.createEncodedVideoStreams) {
						if(sender.track.kind === "audio" && config.senderTransforms["audio"]) {
							senderStreams = sender.createEncodedAudioStreams();
						} else if(sender.track.kind === "video" && config.senderTransforms["video"]) {
							senderStreams = sender.createEncodedVideoStreams();
						}
					}
					if(senderStreams) {
						console.log(senderStreams);
						if(senderStreams.readableStream && senderStreams.writableStream) {
							senderStreams.readableStream
								.pipeThrough(config.senderTransforms[sender.track.kind])
								.pipeTo(senderStreams.writableStream);
						} else if(senderStreams.readable && senderStreams.writable) {
							senderStreams.readable
								.pipeThrough(config.senderTransforms[sender.track.kind])
								.pipeTo(senderStreams.writable);
						}
					}
				}
			});
		}
		// Any data channel to create?
		if(isDataEnabled(media) && !config.dataChannel[Janus.dataChanDefaultLabel]) {
			Janus.log("Creating default data channel");
			createDataChannel(handleId, Janus.dataChanDefaultLabel, null, false);
			config.pc.ondatachannel = function(event) {
				Janus.log("Data channel created by Janus:", event);
				createDataChannel(handleId, event.channel.label, event.channel.protocol, event.channel);
			};
		}
		// If there's a new local stream, let's notify the application
		if(config.myStream) {
			pluginHandle.onlocalstream(config.myStream);
		}
		// Create offer/answer now
		if(!jsep) {
			createOffer(handleId, media, callbacks);
		} else {
			config.pc.setRemoteDescription(jsep)
				.then(function() {
					Janus.log("Remote description accepted!");
					config.remoteSdp = jsep.sdp;
					// Any trickle candidate we cached?
					if(config.candidates && config.candidates.length > 0) {
						for(var i = 0; i< config.candidates.length; i++) {
							var candidate = config.candidates[i];
							Janus.debug("Adding remote candidate:", candidate);
							if(!candidate || candidate.completed === true) {
								// end-of-candidates
								config.pc.addIceCandidate(Janus.endOfCandidates);
							} else {
								// New candidate
								config.pc.addIceCandidate(candidate);
							}
						}
						config.candidates = [];
					}
					// Create the answer now
					createAnswer(handleId, media, callbacks);
				}, callbacks.error);
		}
	}

	function prepareWebrtc(handleId, offer, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : webrtcError;
		var jsep = callbacks.jsep;
		if(offer && jsep) {
			Janus.error("Provided a JSEP to a createOffer");
			callbacks.error("Provided a JSEP to a createOffer");
			return;
		} else if(!offer && (!jsep || !jsep.type || !jsep.sdp)) {
			Janus.error("A valid JSEP is required for createAnswer");
			callbacks.error("A valid JSEP is required for createAnswer");
			return;
		}
		/* Check that callbacks.media is a (not null) Object */
		callbacks.media = (typeof callbacks.media === 'object' && callbacks.media) ? callbacks.media : { audio: true, video: true };
		var media = callbacks.media;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		config.trickle = isTrickleEnabled(callbacks.trickle);
		// Are we updating a session?
		if(!config.pc) {
			// Nope, new PeerConnection
			media.update = false;
			media.keepAudio = false;
			media.keepVideo = false;
		} else {
			Janus.log("Updating existing media session");
			media.update = true;
			// Check if there's anything to add/remove/replace, or if we
			// can go directly to preparing the new SDP offer or answer
			if(callbacks.stream) {
				// External stream: is this the same as the one we were using before?
				if(callbacks.stream !== config.myStream) {
					Janus.log("Renegotiation involves a new external stream");
				}
			} else {
				// Check if there are changes on audio
				if(media.addAudio) {
					media.keepAudio = false;
					media.replaceAudio = false;
					media.removeAudio = false;
					media.audioSend = true;
					if(config.myStream && config.myStream.getAudioTracks() && config.myStream.getAudioTracks().length) {
						Janus.error("Can't add audio stream, there already is one");
						callbacks.error("Can't add audio stream, there already is one");
						return;
					}
				} else if(media.removeAudio) {
					media.keepAudio = false;
					media.replaceAudio = false;
					media.addAudio = false;
					media.audioSend = false;
				} else if(media.replaceAudio) {
					media.keepAudio = false;
					media.addAudio = false;
					media.removeAudio = false;
					media.audioSend = true;
				}
				if(!config.myStream) {
					// No media stream: if we were asked to replace, it's actually an "add"
					if(media.replaceAudio) {
						media.keepAudio = false;
						media.replaceAudio = false;
						media.addAudio = true;
						media.audioSend = true;
					}
					if(isAudioSendEnabled(media)) {
						media.keepAudio = false;
						media.addAudio = true;
					}
				} else {
					if(!config.myStream.getAudioTracks() || config.myStream.getAudioTracks().length === 0) {
						// No audio track: if we were asked to replace, it's actually an "add"
						if(media.replaceAudio) {
							media.keepAudio = false;
							media.replaceAudio = false;
							media.addAudio = true;
							media.audioSend = true;
						}
						if(isAudioSendEnabled(media)) {
							media.keepAudio = false;
							media.addAudio = true;
						}
					} else {
						// We have an audio track: should we keep it as it is?
						if(isAudioSendEnabled(media) &&
								!media.removeAudio && !media.replaceAudio) {
							media.keepAudio = true;
						}
					}
				}
				// Check if there are changes on video
				if(media.addVideo) {
					media.keepVideo = false;
					media.replaceVideo = false;
					media.removeVideo = false;
					media.videoSend = true;
					if(config.myStream && config.myStream.getVideoTracks() && config.myStream.getVideoTracks().length) {
						Janus.error("Can't add video stream, there already is one");
						callbacks.error("Can't add video stream, there already is one");
						return;
					}
				} else if(media.removeVideo) {
					media.keepVideo = false;
					media.replaceVideo = false;
					media.addVideo = false;
					media.videoSend = false;
				} else if(media.replaceVideo) {
					media.keepVideo = false;
					media.addVideo = false;
					media.removeVideo = false;
					media.videoSend = true;
				}
				if(!config.myStream) {
					// No media stream: if we were asked to replace, it's actually an "add"
					if(media.replaceVideo) {
						media.keepVideo = false;
						media.replaceVideo = false;
						media.addVideo = true;
						media.videoSend = true;
					}
					if(isVideoSendEnabled(media)) {
						media.keepVideo = false;
						media.addVideo = true;
					}
				} else {
					if(!config.myStream.getVideoTracks() || config.myStream.getVideoTracks().length === 0) {
						// No video track: if we were asked to replace, it's actually an "add"
						if(media.replaceVideo) {
							media.keepVideo = false;
							media.replaceVideo = false;
							media.addVideo = true;
							media.videoSend = true;
						}
						if(isVideoSendEnabled(media)) {
							media.keepVideo = false;
							media.addVideo = true;
						}
					} else {
						// We have a video track: should we keep it as it is?
						if(isVideoSendEnabled(media) && !media.removeVideo && !media.replaceVideo) {
							media.keepVideo = true;
						}
					}
				}
				// Data channels can only be added
				if(media.addData) {
					media.data = true;
				}
			}
			// If we're updating and keeping all tracks, let's skip the getUserMedia part
			if((isAudioSendEnabled(media) && media.keepAudio) &&
					(isVideoSendEnabled(media) && media.keepVideo)) {
				pluginHandle.consentDialog(false);
				streamsDone(handleId, jsep, media, callbacks, config.myStream);
				return;
			}
		}
		// If we're updating, check if we need to remove/replace one of the tracks
		if(media.update && !config.streamExternal) {
			if(media.removeAudio || media.replaceAudio) {
				if(config.myStream && config.myStream.getAudioTracks() && config.myStream.getAudioTracks().length) {
					var at = config.myStream.getAudioTracks()[0];
					Janus.log("Removing audio track:", at);
					config.myStream.removeTrack(at);
					try {
						at.stop();
					} catch(e) {}
				}
				if(config.pc.getSenders() && config.pc.getSenders().length) {
					var ra = true;
					if(media.replaceAudio && Janus.unifiedPlan) {
						// We can use replaceTrack
						ra = false;
					}
					if(ra) {
						for(var asnd of config.pc.getSenders()) {
							if(asnd && asnd.track && asnd.track.kind === "audio") {
								Janus.log("Removing audio sender:", asnd);
								config.pc.removeTrack(asnd);
							}
						}
					}
				}
			}
			if(media.removeVideo || media.replaceVideo) {
				if(config.myStream && config.myStream.getVideoTracks() && config.myStream.getVideoTracks().length) {
					var vt = config.myStream.getVideoTracks()[0];
					Janus.log("Removing video track:", vt);
					config.myStream.removeTrack(vt);
					try {
						vt.stop();
					} catch(e) {}
				}
				if(config.pc.getSenders() && config.pc.getSenders().length) {
					var rv = true;
					if(media.replaceVideo && Janus.unifiedPlan) {
						// We can use replaceTrack
						rv = false;
					}
					if(rv) {
						for(var vsnd of config.pc.getSenders()) {
							if(vsnd && vsnd.track && vsnd.track.kind === "video") {
								Janus.log("Removing video sender:", vsnd);
								config.pc.removeTrack(vsnd);
							}
						}
					}
				}
			}
		}
		// Was a MediaStream object passed, or do we need to take care of that?
		if(callbacks.stream) {
			var stream = callbacks.stream;
			Janus.log("MediaStream provided by the application");
			Janus.debug(stream);
			// If this is an update, let's check if we need to release the previous stream
			if(media.update) {
				if(config.myStream && config.myStream !== callbacks.stream && !config.streamExternal) {
					// We're replacing a stream we captured ourselves with an external one
					Janus.stopAllTracks(config.myStream);
					config.myStream = null;
				}
			}
			// Skip the getUserMedia part
			config.streamExternal = true;
			pluginHandle.consentDialog(false);
			streamsDone(handleId, jsep, media, callbacks, stream);
			return;
		}
		if(isAudioSendEnabled(media) || isVideoSendEnabled(media)) {
			if(!Janus.isGetUserMediaAvailable()) {
				callbacks.error("getUserMedia not available");
				return;
			}
			var constraints = { mandatory: {}, optional: []};
			pluginHandle.consentDialog(true);
			var audioSupport = isAudioSendEnabled(media);
			if(audioSupport && media && typeof media.audio === 'object')
				audioSupport = media.audio;
			var videoSupport = isVideoSendEnabled(media);
			if(videoSupport && media) {
				var simulcast = (callbacks.simulcast === true);
				var simulcast2 = (callbacks.simulcast2 === true);
				if((simulcast || simulcast2) && !jsep && !media.video)
					media.video = "hires";
				if(media.video && media.video != 'screen' && media.video != 'window') {
					if(typeof media.video === 'object') {
						videoSupport = media.video;
					} else {
						var width = 0;
						var height = 0, maxHeight = 0;
						if(media.video === 'lowres') {
							// Small resolution, 4:3
							height = 240;
							maxHeight = 240;
							width = 320;
						} else if(media.video === 'lowres-16:9') {
							// Small resolution, 16:9
							height = 180;
							maxHeight = 180;
							width = 320;
						} else if(media.video === 'hires' || media.video === 'hires-16:9' || media.video === 'hdres') {
							// High(HD) resolution is only 16:9
							height = 720;
							maxHeight = 720;
							width = 1280;
						} else if(media.video === 'fhdres') {
							// Full HD resolution is only 16:9
							height = 1080;
							maxHeight = 1080;
							width = 1920;
						} else if(media.video === '4kres') {
							// 4K resolution is only 16:9
							height = 2160;
							maxHeight = 2160;
							width = 3840;
						} else if(media.video === 'stdres') {
							// Normal resolution, 4:3
							height = 480;
							maxHeight = 480;
							width = 640;
						} else if(media.video === 'stdres-16:9') {
							// Normal resolution, 16:9
							height = 360;
							maxHeight = 360;
							width = 640;
						} else {
							Janus.log("Default video setting is stdres 4:3");
							height = 480;
							maxHeight = 480;
							width = 640;
						}
						Janus.log("Adding media constraint:", media.video);
						videoSupport = {
							'height': {'ideal': height},
							'width': {'ideal': width}
						};
						Janus.log("Adding video constraint:", videoSupport);
					}
				} else if(media.video === 'screen' || media.video === 'window') {
					if(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
						// The new experimental getDisplayMedia API is available, let's use that
						// https://groups.google.com/forum/#!topic/discuss-webrtc/Uf0SrR4uxzk
						// https://webrtchacks.com/chrome-screensharing-getdisplaymedia/
						constraints.video = {};
						if(media.screenshareFrameRate) {
							constraints.video.frameRate = media.screenshareFrameRate;
						}
						if(media.screenshareHeight) {
							constraints.video.height = media.screenshareHeight;
						}
						if(media.screenshareWidth) {
							constraints.video.width = media.screenshareWidth;
						}
						constraints.audio = media.captureDesktopAudio;
						navigator.mediaDevices.getDisplayMedia(constraints)
							.then(function(stream) {
								pluginHandle.consentDialog(false);
								if(isAudioSendEnabled(media) && !media.keepAudio) {
									navigator.mediaDevices.getUserMedia({ audio: true, video: false })
									.then(function (audioStream) {
										stream.addTrack(audioStream.getAudioTracks()[0]);
										streamsDone(handleId, jsep, media, callbacks, stream);
									})
								} else {
									streamsDone(handleId, jsep, media, callbacks, stream);
								}
							}, function (error) {
								pluginHandle.consentDialog(false);
								callbacks.error(error);
							});
						return;
					}
					// We're going to try and use the extension for Chrome 34+, the old approach
					// for older versions of Chrome, or the experimental support in Firefox 33+
					function callbackUserMedia (error, stream) {
						pluginHandle.consentDialog(false);
						if(error) {
							callbacks.error(error);
						} else {
							streamsDone(handleId, jsep, media, callbacks, stream);
						}
					}
					function getScreenMedia(constraints, gsmCallback, useAudio) {
						Janus.log("Adding media constraint (screen capture)");
						Janus.debug(constraints);
						navigator.mediaDevices.getUserMedia(constraints)
							.then(function(stream) {
								if(useAudio) {
									navigator.mediaDevices.getUserMedia({ audio: true, video: false })
									.then(function (audioStream) {
										stream.addTrack(audioStream.getAudioTracks()[0]);
										gsmCallback(null, stream);
									})
								} else {
									gsmCallback(null, stream);
								}
							})
							.catch(function(error) { pluginHandle.consentDialog(false); gsmCallback(error); });
					}
					if(Janus.webRTCAdapter.browserDetails.browser === 'chrome') {
						var chromever = Janus.webRTCAdapter.browserDetails.version;
						var maxver = 33;
						if(window.navigator.userAgent.match('Linux'))
							maxver = 35;	// "known" crash in chrome 34 and 35 on linux
						if(chromever >= 26 && chromever <= maxver) {
							// Chrome 26->33 requires some awkward chrome://flags manipulation
							constraints = {
								video: {
									mandatory: {
										googLeakyBucket: true,
										maxWidth: window.screen.width,
										maxHeight: window.screen.height,
										minFrameRate: media.screenshareFrameRate,
										maxFrameRate: media.screenshareFrameRate,
										chromeMediaSource: 'screen'
									}
								},
								audio: isAudioSendEnabled(media) && !media.keepAudio
							};
							getScreenMedia(constraints, callbackUserMedia);
						} else {
							// Chrome 34+ requires an extension
							Janus.extension.getScreen(function (error, sourceId) {
								if (error) {
									pluginHandle.consentDialog(false);
									return callbacks.error(error);
								}
								constraints = {
									audio: false,
									video: {
										mandatory: {
											chromeMediaSource: 'desktop',
											maxWidth: window.screen.width,
											maxHeight: window.screen.height,
											minFrameRate: media.screenshareFrameRate,
											maxFrameRate: media.screenshareFrameRate,
										},
										optional: [
											{googLeakyBucket: true},
											{googTemporalLayeredScreencast: true}
										]
									}
								};
								constraints.video.mandatory.chromeMediaSourceId = sourceId;
								getScreenMedia(constraints, callbackUserMedia,
									isAudioSendEnabled(media) && !media.keepAudio);
							});
						}
					} else if(Janus.webRTCAdapter.browserDetails.browser === 'firefox') {
						if(Janus.webRTCAdapter.browserDetails.version >= 33) {
							// Firefox 33+ has experimental support for screen sharing
							constraints = {
								video: {
									mozMediaSource: media.video,
									mediaSource: media.video
								},
								audio: isAudioSendEnabled(media) && !media.keepAudio
							};
							getScreenMedia(constraints, function (err, stream) {
								callbackUserMedia(err, stream);
								// Workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=1045810
								if (!err) {
									var lastTime = stream.currentTime;
									var polly = window.setInterval(function () {
										if(!stream)
											window.clearInterval(polly);
										if(stream.currentTime == lastTime) {
											window.clearInterval(polly);
											if(stream.onended) {
												stream.onended();
											}
										}
										lastTime = stream.currentTime;
									}, 500);
								}
							});
						} else {
							var error = new Error('NavigatorUserMediaError');
							error.name = 'Your version of Firefox does not support screen sharing, please install Firefox 33 (or more recent versions)';
							pluginHandle.consentDialog(false);
							callbacks.error(error);
							return;
						}
					}
					return;
				}
			}
			// If we got here, we're not screensharing
			if(!media || media.video !== 'screen') {
				// Check whether all media sources are actually available or not
				navigator.mediaDevices.enumerateDevices().then(function(devices) {
					var audioExist = devices.some(function(device) {
						return device.kind === 'audioinput';
					}),
					videoExist = isScreenSendEnabled(media) || devices.some(function(device) {
						return device.kind === 'videoinput';
					});

					// Check whether a missing device is really a problem
					var audioSend = isAudioSendEnabled(media);
					var videoSend = isVideoSendEnabled(media);
					var needAudioDevice = isAudioSendRequired(media);
					var needVideoDevice = isVideoSendRequired(media);
					if(audioSend || videoSend || needAudioDevice || needVideoDevice) {
						// We need to send either audio or video
						var haveAudioDevice = audioSend ? audioExist : false;
						var haveVideoDevice = videoSend ? videoExist : false;
						if(!haveAudioDevice && !haveVideoDevice) {
							// FIXME Should we really give up, or just assume recvonly for both?
							pluginHandle.consentDialog(false);
							callbacks.error('No capture device found');
							return false;
						} else if(!haveAudioDevice && needAudioDevice) {
							pluginHandle.consentDialog(false);
							callbacks.error('Audio capture is required, but no capture device found');
							return false;
						} else if(!haveVideoDevice && needVideoDevice) {
							pluginHandle.consentDialog(false);
							callbacks.error('Video capture is required, but no capture device found');
							return false;
						}
					}

					var gumConstraints = {
						audio: (audioExist && !media.keepAudio) ? audioSupport : false,
						video: (videoExist && !media.keepVideo) ? videoSupport : false
					};
					Janus.debug("getUserMedia constraints", gumConstraints);
					if (!gumConstraints.audio && !gumConstraints.video) {
						pluginHandle.consentDialog(false);
						streamsDone(handleId, jsep, media, callbacks, stream);
					} else {
						navigator.mediaDevices.getUserMedia(gumConstraints)
							.then(function(stream) {
								pluginHandle.consentDialog(false);
								streamsDone(handleId, jsep, media, callbacks, stream);
							}).catch(function(error) {
								pluginHandle.consentDialog(false);
								callbacks.error({code: error.code, name: error.name, message: error.message});
							});
					}
				})
				.catch(function(error) {
					pluginHandle.consentDialog(false);
					callbacks.error(error);
				});
			}
		} else {
			// No need to do a getUserMedia, create offer/answer right away
			streamsDone(handleId, jsep, media, callbacks);
		}
	}

	function prepareWebrtcPeer(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : webrtcError;
		var jsep = callbacks.jsep;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		if(jsep) {
			if(!config.pc) {
				Janus.warn("Wait, no PeerConnection?? if this is an answer, use createAnswer and not handleRemoteJsep");
				callbacks.error("No PeerConnection: if this is an answer, use createAnswer and not handleRemoteJsep");
				return;
			}
			config.pc.setRemoteDescription(jsep)
				.then(function() {
					Janus.log("Remote description accepted!");
					config.remoteSdp = jsep.sdp;
					// Any trickle candidate we cached?
					if(config.candidates && config.candidates.length > 0) {
						for(var i = 0; i< config.candidates.length; i++) {
							var candidate = config.candidates[i];
							Janus.debug("Adding remote candidate:", candidate);
							if(!candidate || candidate.completed === true) {
								// end-of-candidates
								config.pc.addIceCandidate(Janus.endOfCandidates);
							} else {
								// New candidate
								config.pc.addIceCandidate(candidate);
							}
						}
						config.candidates = [];
					}
					// Done
					callbacks.success();
				}, callbacks.error);
		} else {
			callbacks.error("Invalid JSEP");
		}
	}

	function createOffer(handleId, media, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		callbacks.customizeSdp = (typeof callbacks.customizeSdp == "function") ? callbacks.customizeSdp : Janus.noop;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		var simulcast = (callbacks.simulcast === true);
		if(!simulcast) {
			Janus.log("Creating offer (iceDone=" + config.iceDone + ")");
		} else {
			Janus.log("Creating offer (iceDone=" + config.iceDone + ", simulcast=" + simulcast + ")");
		}
		// https://code.google.com/p/webrtc/issues/detail?id=3508
		var mediaConstraints = {};
		if(Janus.unifiedPlan) {
			// We can use Transceivers
			var audioTransceiver = null, videoTransceiver = null;
			var transceivers = config.pc.getTransceivers();
			if(transceivers && transceivers.length > 0) {
				for(var t of transceivers) {
					if((t.sender && t.sender.track && t.sender.track.kind === "audio") ||
							(t.receiver && t.receiver.track && t.receiver.track.kind === "audio")) {
						if(!audioTransceiver) {
							audioTransceiver = t;
						}
						continue;
					}
					if((t.sender && t.sender.track && t.sender.track.kind === "video") ||
							(t.receiver && t.receiver.track && t.receiver.track.kind === "video")) {
						if(!videoTransceiver) {
							videoTransceiver = t;
						}
						continue;
					}
				}
			}
			// Handle audio (and related changes, if any)
			var audioSend = isAudioSendEnabled(media);
			var audioRecv = isAudioRecvEnabled(media);
			if(!audioSend && !audioRecv) {
				// Audio disabled: have we removed it?
				if(media.removeAudio && audioTransceiver) {
					if (audioTransceiver.setDirection) {
						audioTransceiver.setDirection("inactive");
					} else {
						audioTransceiver.direction = "inactive";
					}
					Janus.log("Setting audio transceiver to inactive:", audioTransceiver);
				}
			} else {
				// Take care of audio m-line
				if(audioSend && audioRecv) {
					if(audioTransceiver) {
						if (audioTransceiver.setDirection) {
							audioTransceiver.setDirection("sendrecv");
						} else {
							audioTransceiver.direction = "sendrecv";
						}
						Janus.log("Setting audio transceiver to sendrecv:", audioTransceiver);
					}
				} else if(audioSend && !audioRecv) {
					if(audioTransceiver) {
						if (audioTransceiver.setDirection) {
							audioTransceiver.setDirection("sendonly");
						} else {
							audioTransceiver.direction = "sendonly";
						}
						Janus.log("Setting audio transceiver to sendonly:", audioTransceiver);
					}
				} else if(!audioSend && audioRecv) {
					if(audioTransceiver) {
						if (audioTransceiver.setDirection) {
							audioTransceiver.setDirection("recvonly");
						} else {
							audioTransceiver.direction = "recvonly";
						}
						Janus.log("Setting audio transceiver to recvonly:", audioTransceiver);
					} else {
						// In theory, this is the only case where we might not have a transceiver yet
						audioTransceiver = config.pc.addTransceiver("audio", { direction: "recvonly" });
						Janus.log("Adding recvonly audio transceiver:", audioTransceiver);
					}
				}
			}
			// Handle video (and related changes, if any)
			var videoSend = isVideoSendEnabled(media);
			var videoRecv = isVideoRecvEnabled(media);
			if(!videoSend && !videoRecv) {
				// Video disabled: have we removed it?
				if(media.removeVideo && videoTransceiver) {
					if (videoTransceiver.setDirection) {
						videoTransceiver.setDirection("inactive");
					} else {
						videoTransceiver.direction = "inactive";
					}
					Janus.log("Setting video transceiver to inactive:", videoTransceiver);
				}
			} else {
				// Take care of video m-line
				if(videoSend && videoRecv) {
					if(videoTransceiver) {
						if (videoTransceiver.setDirection) {
							videoTransceiver.setDirection("sendrecv");
						} else {
							videoTransceiver.direction = "sendrecv";
						}
						Janus.log("Setting video transceiver to sendrecv:", videoTransceiver);
					}
				} else if(videoSend && !videoRecv) {
					if(videoTransceiver) {
						if (videoTransceiver.setDirection) {
							videoTransceiver.setDirection("sendonly");
						} else {
							videoTransceiver.direction = "sendonly";
						}
						Janus.log("Setting video transceiver to sendonly:", videoTransceiver);
					}
				} else if(!videoSend && videoRecv) {
					if(videoTransceiver) {
						if (videoTransceiver.setDirection) {
							videoTransceiver.setDirection("recvonly");
						} else {
							videoTransceiver.direction = "recvonly";
						}
						Janus.log("Setting video transceiver to recvonly:", videoTransceiver);
					} else {
						// In theory, this is the only case where we might not have a transceiver yet
						videoTransceiver = config.pc.addTransceiver("video", { direction: "recvonly" });
						Janus.log("Adding recvonly video transceiver:", videoTransceiver);
					}
				}
			}
		} else {
			mediaConstraints["offerToReceiveAudio"] = isAudioRecvEnabled(media);
			mediaConstraints["offerToReceiveVideo"] = isVideoRecvEnabled(media);
		}
		var iceRestart = (callbacks.iceRestart === true);
		if(iceRestart) {
			mediaConstraints["iceRestart"] = true;
		}
		Janus.debug(mediaConstraints);
		// Check if this is Firefox and we've been asked to do simulcasting
		var sendVideo = isVideoSendEnabled(media);
		if(sendVideo && simulcast && Janus.webRTCAdapter.browserDetails.browser === "firefox") {
			// FIXME Based on https://gist.github.com/voluntas/088bc3cc62094730647b
			Janus.log("Enabling Simulcasting for Firefox (RID)");
			var sender = config.pc.getSenders().find(function(s) {return s.track.kind === "video"});
			if(sender) {
				var parameters = sender.getParameters();
				if(!parameters) {
					parameters = {};
				}
				var maxBitrates = getMaxBitrates(callbacks.simulcastMaxBitrates);
				parameters.encodings = callbacks.sendEncodings || [
					{ rid: "h", active: true, maxBitrate: maxBitrates.high },
					{ rid: "m", active: true, maxBitrate: maxBitrates.medium, scaleResolutionDownBy: 2 },
					{ rid: "l", active: true, maxBitrate: maxBitrates.low, scaleResolutionDownBy: 4 }
				];
				sender.setParameters(parameters);
			}
		}
		config.pc.createOffer(mediaConstraints)
			.then(function(offer) {
				Janus.debug(offer);
				// JSON.stringify doesn't work on some WebRTC objects anymore
				// See https://code.google.com/p/chromium/issues/detail?id=467366
				var jsep = {
					"type": offer.type,
					"sdp": offer.sdp
				};
				callbacks.customizeSdp(jsep);
				offer.sdp = jsep.sdp;
				Janus.log("Setting local description");
				if(sendVideo && simulcast) {
					// This SDP munging only works with Chrome (Safari STP may support it too)
					if(Janus.webRTCAdapter.browserDetails.browser === "chrome" ||
							Janus.webRTCAdapter.browserDetails.browser === "safari") {
						Janus.log("Enabling Simulcasting for Chrome (SDP munging)");
						offer.sdp = mungeSdpForSimulcasting(offer.sdp);
					} else if(Janus.webRTCAdapter.browserDetails.browser !== "firefox") {
						Janus.warn("simulcast=true, but this is not Chrome nor Firefox, ignoring");
					}
				}
				config.mySdp = offer.sdp;
				config.pc.setLocalDescription(offer)
					.catch(callbacks.error);
				config.mediaConstraints = mediaConstraints;
				if(!config.iceDone && !config.trickle) {
					// Don't do anything until we have all candidates
					Janus.log("Waiting for all candidates...");
					return;
				}
				// If transforms are present, notify Janus that the media is end-to-end encrypted
				if(config.senderTransforms || config.receiverTransforms) {
					offer["e2ee"] = true;
				}
				callbacks.success(offer);
			}, callbacks.error);
	}

	function createAnswer(handleId, media, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		callbacks.customizeSdp = (typeof callbacks.customizeSdp == "function") ? callbacks.customizeSdp : Janus.noop;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			callbacks.error("Invalid handle");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		var simulcast = (callbacks.simulcast === true);
		if(!simulcast) {
			Janus.log("Creating answer (iceDone=" + config.iceDone + ")");
		} else {
			Janus.log("Creating answer (iceDone=" + config.iceDone + ", simulcast=" + simulcast + ")");
		}
		var mediaConstraints = null;
		if(Janus.unifiedPlan) {
			// We can use Transceivers
			mediaConstraints = {};
			var audioTransceiver = null, videoTransceiver = null;
			var transceivers = config.pc.getTransceivers();
			if(transceivers && transceivers.length > 0) {
				for(var t of transceivers) {
					if((t.sender && t.sender.track && t.sender.track.kind === "audio") ||
							(t.receiver && t.receiver.track && t.receiver.track.kind === "audio")) {
						if(!audioTransceiver)
							audioTransceiver = t;
						continue;
					}
					if((t.sender && t.sender.track && t.sender.track.kind === "video") ||
							(t.receiver && t.receiver.track && t.receiver.track.kind === "video")) {
						if(!videoTransceiver)
							videoTransceiver = t;
						continue;
					}
				}
			}
			// Handle audio (and related changes, if any)
			var audioSend = isAudioSendEnabled(media);
			var audioRecv = isAudioRecvEnabled(media);
			if(!audioSend && !audioRecv) {
				// Audio disabled: have we removed it?
				if(media.removeAudio && audioTransceiver) {
					try {
						if (audioTransceiver.setDirection) {
							audioTransceiver.setDirection("inactive");
						} else {
							audioTransceiver.direction = "inactive";
						}
						Janus.log("Setting audio transceiver to inactive:", audioTransceiver);
					} catch(e) {
						Janus.error(e);
					}
				}
			} else {
				// Take care of audio m-line
				if(audioSend && audioRecv) {
					if(audioTransceiver) {
						try {
							if (audioTransceiver.setDirection) {
								audioTransceiver.setDirection("sendrecv");
							} else {
								audioTransceiver.direction = "sendrecv";
							}
							Janus.log("Setting audio transceiver to sendrecv:", audioTransceiver);
						} catch(e) {
							Janus.error(e);
						}
					}
				} else if(audioSend && !audioRecv) {
					try {
						if(audioTransceiver) {
							if (audioTransceiver.setDirection) {
								audioTransceiver.setDirection("sendonly");
							} else {
								audioTransceiver.direction = "sendonly";
							}
							Janus.log("Setting audio transceiver to sendonly:", audioTransceiver);
						}
					} catch(e) {
						Janus.error(e);
					}
				} else if(!audioSend && audioRecv) {
					if(audioTransceiver) {
						try {
							if (audioTransceiver.setDirection) {
								audioTransceiver.setDirection("recvonly");
							} else {
								audioTransceiver.direction = "recvonly";
							}
							Janus.log("Setting audio transceiver to recvonly:", audioTransceiver);
						} catch(e) {
							Janus.error(e);
						}
					} else {
						// In theory, this is the only case where we might not have a transceiver yet
						audioTransceiver = config.pc.addTransceiver("audio", { direction: "recvonly" });
						Janus.log("Adding recvonly audio transceiver:", audioTransceiver);
					}
				}
			}
			// Handle video (and related changes, if any)
			var videoSend = isVideoSendEnabled(media);
			var videoRecv = isVideoRecvEnabled(media);
			if(!videoSend && !videoRecv) {
				// Video disabled: have we removed it?
				if(media.removeVideo && videoTransceiver) {
					try {
						if (videoTransceiver.setDirection) {
							videoTransceiver.setDirection("inactive");
						} else {
							videoTransceiver.direction = "inactive";
						}
						Janus.log("Setting video transceiver to inactive:", videoTransceiver);
					} catch(e) {
						Janus.error(e);
					}
				}
			} else {
				// Take care of video m-line
				if(videoSend && videoRecv) {
					if(videoTransceiver) {
						try {
							if (videoTransceiver.setDirection) {
								videoTransceiver.setDirection("sendrecv");
							} else {
								videoTransceiver.direction = "sendrecv";
							}
							Janus.log("Setting video transceiver to sendrecv:", videoTransceiver);
						} catch(e) {
							Janus.error(e);
						}
					}
				} else if(videoSend && !videoRecv) {
					if(videoTransceiver) {
						try {
							if (videoTransceiver.setDirection) {
								videoTransceiver.setDirection("sendonly");
							} else {
								videoTransceiver.direction = "sendonly";
							}
							Janus.log("Setting video transceiver to sendonly:", videoTransceiver);
						} catch(e) {
							Janus.error(e);
						}
					}
				} else if(!videoSend && videoRecv) {
					if(videoTransceiver) {
						try {
							if (videoTransceiver.setDirection) {
								videoTransceiver.setDirection("recvonly");
							} else {
								videoTransceiver.direction = "recvonly";
							}
							Janus.log("Setting video transceiver to recvonly:", videoTransceiver);
						} catch(e) {
							Janus.error(e);
						}
					} else {
						// In theory, this is the only case where we might not have a transceiver yet
						videoTransceiver = config.pc.addTransceiver("video", { direction: "recvonly" });
						Janus.log("Adding recvonly video transceiver:", videoTransceiver);
					}
				}
			}
		} else {
			if(Janus.webRTCAdapter.browserDetails.browser === "firefox" || Janus.webRTCAdapter.browserDetails.browser === "edge") {
				mediaConstraints = {
					offerToReceiveAudio: isAudioRecvEnabled(media),
					offerToReceiveVideo: isVideoRecvEnabled(media)
				};
			} else {
				mediaConstraints = {
					mandatory: {
						OfferToReceiveAudio: isAudioRecvEnabled(media),
						OfferToReceiveVideo: isVideoRecvEnabled(media)
					}
				};
			}
		}
		Janus.debug(mediaConstraints);
		// Check if this is Firefox and we've been asked to do simulcasting
		var sendVideo = isVideoSendEnabled(media);
		if(sendVideo && simulcast && Janus.webRTCAdapter.browserDetails.browser === "firefox") {
			// FIXME Based on https://gist.github.com/voluntas/088bc3cc62094730647b
			Janus.log("Enabling Simulcasting for Firefox (RID)");
			var sender = config.pc.getSenders()[1];
			Janus.log(sender);
			var parameters = sender.getParameters();
			Janus.log(parameters);

			var maxBitrates = getMaxBitrates(callbacks.simulcastMaxBitrates);
			sender.setParameters({encodings: callbacks.sendEncodings || [
				{ rid: "h", active: true, maxBitrate: maxBitrates.high },
				{ rid: "m", active: true, maxBitrate: maxBitrates.medium, scaleResolutionDownBy: 2},
				{ rid: "l", active: true, maxBitrate: maxBitrates.low, scaleResolutionDownBy: 4}
			]});
		}
		config.pc.createAnswer(mediaConstraints)
			.then(function(answer) {
				Janus.debug(answer);
				// JSON.stringify doesn't work on some WebRTC objects anymore
				// See https://code.google.com/p/chromium/issues/detail?id=467366
				var jsep = {
					"type": answer.type,
					"sdp": answer.sdp
				};
				callbacks.customizeSdp(jsep);
				answer.sdp = jsep.sdp;
				Janus.log("Setting local description");
				if(sendVideo && simulcast) {
					// This SDP munging only works with Chrome
					if(Janus.webRTCAdapter.browserDetails.browser === "chrome") {
						// FIXME Apparently trying to simulcast when answering breaks video in Chrome...
						//~ Janus.log("Enabling Simulcasting for Chrome (SDP munging)");
						//~ answer.sdp = mungeSdpForSimulcasting(answer.sdp);
						Janus.warn("simulcast=true, but this is an answer, and video breaks in Chrome if we enable it");
					} else if(Janus.webRTCAdapter.browserDetails.browser !== "firefox") {
						Janus.warn("simulcast=true, but this is not Chrome nor Firefox, ignoring");
					}
				}
				config.mySdp = answer.sdp;
				config.pc.setLocalDescription(answer)
					.catch(callbacks.error);
				config.mediaConstraints = mediaConstraints;
				if(!config.iceDone && !config.trickle) {
					// Don't do anything until we have all candidates
					Janus.log("Waiting for all candidates...");
					return;
				}
				// If transforms are present, notify Janus that the media is end-to-end encrypted
				if(config.senderTransforms || config.receiverTransforms) {
					answer["e2ee"] = true;
				}
				callbacks.success(answer);
			}, callbacks.error);
	}

	function sendSDP(handleId, callbacks) {
		callbacks = callbacks || {};
		callbacks.success = (typeof callbacks.success == "function") ? callbacks.success : Janus.noop;
		callbacks.error = (typeof callbacks.error == "function") ? callbacks.error : Janus.noop;
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle, not sending anything");
			return;
		}
		var config = pluginHandle.webrtcStuff;
		Janus.log("Sending offer/answer SDP...");
		if(!config.mySdp) {
			Janus.warn("Local SDP instance is invalid, not sending anything...");
			return;
		}
		config.mySdp = {
			"type": config.pc.localDescription.type,
			"sdp": config.pc.localDescription.sdp
		};
		if(config.trickle === false)
			config.mySdp["trickle"] = false;
		Janus.debug(callbacks);
		config.sdpSent = true;
		callbacks.success(config.mySdp);
	}

	function getVolume(handleId, remote) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return 0;
		}
		var stream = remote ? "remote" : "local";
		var config = pluginHandle.webrtcStuff;
		if(!config.volume[stream])
			config.volume[stream] = { value: 0 };
		// Start getting the volume, if audioLevel in getStats is supported (apparently
		// they're only available in Chrome/Safari right now: https://webrtc-stats.callstats.io/)
		if(config.pc.getStats && (Janus.webRTCAdapter.browserDetails.browser === "chrome" ||
				Janus.webRTCAdapter.browserDetails.browser === "safari")) {
			if(remote && !config.remoteStream) {
				Janus.warn("Remote stream unavailable");
				return 0;
			} else if(!remote && !config.myStream) {
				Janus.warn("Local stream unavailable");
				return 0;
			}
			if(!config.volume[stream].timer) {
				Janus.log("Starting " + stream + " volume monitor");
				config.volume[stream].timer = setInterval(function() {
					config.pc.getStats()
						.then(function(stats) {
							stats.forEach(function (res) {
								if(!res || res.kind !== "audio")
									return;
								if((remote && !res.remoteSource) || (!remote && res.type !== "media-source"))
									return;
								config.volume[stream].value = (res.audioLevel ? res.audioLevel : 0);
							});
						});
				}, 200);
				return 0;	// We don't have a volume to return yet
			}
			return config.volume[stream].value;
		} else {
			// audioInputLevel and audioOutputLevel seem only available in Chrome? audioLevel
			// seems to be available on Chrome and Firefox, but they don't seem to work
			Janus.warn("Getting the " + stream + " volume unsupported by browser");
			return 0;
		}
	}

	function isMuted(handleId, video) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return true;
		}
		var config = pluginHandle.webrtcStuff;
		if(!config.pc) {
			Janus.warn("Invalid PeerConnection");
			return true;
		}
		if(!config.myStream) {
			Janus.warn("Invalid local MediaStream");
			return true;
		}
		if(video) {
			// Check video track
			if(!config.myStream.getVideoTracks() || config.myStream.getVideoTracks().length === 0) {
				Janus.warn("No video track");
				return true;
			}
			return !config.myStream.getVideoTracks()[0].enabled;
		} else {
			// Check audio track
			if(!config.myStream.getAudioTracks() || config.myStream.getAudioTracks().length === 0) {
				Janus.warn("No audio track");
				return true;
			}
			return !config.myStream.getAudioTracks()[0].enabled;
		}
	}

	function mute(handleId, video, mute) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return false;
		}
		var config = pluginHandle.webrtcStuff;
		if(!config.pc) {
			Janus.warn("Invalid PeerConnection");
			return false;
		}
		if(!config.myStream) {
			Janus.warn("Invalid local MediaStream");
			return false;
		}
		if(video) {
			// Mute/unmute video track
			if(!config.myStream.getVideoTracks() || config.myStream.getVideoTracks().length === 0) {
				Janus.warn("No video track");
				return false;
			}
			config.myStream.getVideoTracks()[0].enabled = !mute;
			return true;
		} else {
			// Mute/unmute audio track
			if(!config.myStream.getAudioTracks() || config.myStream.getAudioTracks().length === 0) {
				Janus.warn("No audio track");
				return false;
			}
			config.myStream.getAudioTracks()[0].enabled = !mute;
			return true;
		}
	}

	function getBitrate(handleId) {
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle || !pluginHandle.webrtcStuff) {
			Janus.warn("Invalid handle");
			return "Invalid handle";
		}
		var config = pluginHandle.webrtcStuff;
		if(!config.pc)
			return "Invalid PeerConnection";
		// Start getting the bitrate, if getStats is supported
		if(config.pc.getStats) {
			if(!config.bitrate.timer) {
				Janus.log("Starting bitrate timer (via getStats)");
				config.bitrate.timer = setInterval(function() {
					config.pc.getStats()
						.then(function(stats) {
							stats.forEach(function (res) {
								if(!res)
									return;
								var inStats = false;
								// Check if these are statistics on incoming media
								if((res.mediaType === "video" || res.id.toLowerCase().indexOf("video") > -1) &&
										res.type === "inbound-rtp" && res.id.indexOf("rtcp") < 0) {
									// New stats
									inStats = true;
								} else if(res.type == 'ssrc' && res.bytesReceived &&
										(res.googCodecName === "VP8" || res.googCodecName === "")) {
									// Older Chromer versions
									inStats = true;
								}
								// Parse stats now
								if(inStats) {
									config.bitrate.bsnow = res.bytesReceived;
									config.bitrate.tsnow = res.timestamp;
									if(config.bitrate.bsbefore === null || config.bitrate.tsbefore === null) {
										// Skip this round
										config.bitrate.bsbefore = config.bitrate.bsnow;
										config.bitrate.tsbefore = config.bitrate.tsnow;
									} else {
										// Calculate bitrate
										var timePassed = config.bitrate.tsnow - config.bitrate.tsbefore;
										if(Janus.webRTCAdapter.browserDetails.browser === "safari")
											timePassed = timePassed/1000;	// Apparently the timestamp is in microseconds, in Safari
										var bitRate = Math.round((config.bitrate.bsnow - config.bitrate.bsbefore) * 8 / timePassed);
										if(Janus.webRTCAdapter.browserDetails.browser === "safari")
											bitRate = parseInt(bitRate/1000);
										config.bitrate.value = bitRate + ' kbits/sec';
										//~ Janus.log("Estimated bitrate is " + config.bitrate.value);
										config.bitrate.bsbefore = config.bitrate.bsnow;
										config.bitrate.tsbefore = config.bitrate.tsnow;
									}
								}
							});
						});
				}, 1000);
				return "0 kbits/sec";	// We don't have a bitrate value yet
			}
			return config.bitrate.value;
		} else {
			Janus.warn("Getting the video bitrate unsupported by browser");
			return "Feature unsupported by browser";
		}
	}

	function webrtcError(error) {
		Janus.error("WebRTC error:", error);
	}

	function cleanupWebrtc(handleId, hangupRequest) {
		Janus.log("Cleaning WebRTC stuff");
		var pluginHandle = pluginHandles[handleId];
		if(!pluginHandle) {
			// Nothing to clean
			return;
		}
		var config = pluginHandle.webrtcStuff;
		if(config) {
			if(hangupRequest === true) {
				// Send a hangup request (we don't really care about the response)
				var request = { "janus": "hangup", "transaction": Janus.randomString(12) };
				if(pluginHandle.token)
					request["token"] = pluginHandle.token;
				if(apisecret)
					request["apisecret"] = apisecret;
				Janus.debug("Sending hangup request (handle=" + handleId + "):");
				Janus.debug(request);
				if(websockets) {
					request["session_id"] = sessionId;
					request["handle_id"] = handleId;
					ws.send(JSON.stringify(request));
				} else {
					Janus.httpAPICall(server + "/" + sessionId + "/" + handleId, {
						verb: 'POST',
						withCredentials: withCredentials,
						body: request
					});
				}
			}
			// Cleanup stack
			config.remoteStream = null;
			if(config.volume) {
				if(config.volume["local"] && config.volume["local"].timer)
					clearInterval(config.volume["local"].timer);
				if(config.volume["remote"] && config.volume["remote"].timer)
					clearInterval(config.volume["remote"].timer);
			}
			config.volume = {};
			if(config.bitrate.timer)
				clearInterval(config.bitrate.timer);
			config.bitrate.timer = null;
			config.bitrate.bsnow = null;
			config.bitrate.bsbefore = null;
			config.bitrate.tsnow = null;
			config.bitrate.tsbefore = null;
			config.bitrate.value = null;
			if(!config.streamExternal && config.myStream) {
				Janus.log("Stopping local stream tracks");
				Janus.stopAllTracks(config.myStream);
			}
			config.streamExternal = false;
			config.myStream = null;
			// Close PeerConnection
			try {
				config.pc.close();
			} catch(e) {
				// Do nothing
			}
			config.pc = null;
			config.candidates = null;
			config.mySdp = null;
			config.remoteSdp = null;
			config.iceDone = false;
			config.dataChannel = {};
			config.dtmfSender = null;
			config.senderTransforms = null;
			config.receiverTransforms = null;
		}
		pluginHandle.oncleanup();
	}

	// Helper method to munge an SDP to enable simulcasting (Chrome only)
	function mungeSdpForSimulcasting(sdp) {
		// Let's munge the SDP to add the attributes for enabling simulcasting
		// (based on https://gist.github.com/ggarber/a19b4c33510028b9c657)
		var lines = sdp.split("\r\n");
		var video = false;
		var ssrc = [ -1 ], ssrc_fid = [ -1 ];
		var cname = null, msid = null, mslabel = null, label = null;
		var insertAt = -1;
		for(var i=0; i<lines.length; i++) {
			var mline = lines[i].match(/m=(\w+) */);
			if(mline) {
				var medium = mline[1];
				if(medium === "video") {
					// New video m-line: make sure it's the first one
					if(ssrc[0] < 0) {
						video = true;
					} else {
						// We're done, let's add the new attributes here
						insertAt = i;
						break;
					}
				} else {
					// New non-video m-line: do we have what we were looking for?
					if(ssrc[0] > -1) {
						// We're done, let's add the new attributes here
						insertAt = i;
						break;
					}
				}
				continue;
			}
			if(!video)
				continue;
			var fid = lines[i].match(/a=ssrc-group:FID (\d+) (\d+)/);
			if(fid) {
				ssrc[0] = fid[1];
				ssrc_fid[0] = fid[2];
				lines.splice(i, 1); i--;
				continue;
			}
			if(ssrc[0]) {
				var match = lines[i].match('a=ssrc:' + ssrc[0] + ' cname:(.+)')
				if(match) {
					cname = match[1];
				}
				match = lines[i].match('a=ssrc:' + ssrc[0] + ' msid:(.+)')
				if(match) {
					msid = match[1];
				}
				match = lines[i].match('a=ssrc:' + ssrc[0] + ' mslabel:(.+)')
				if(match) {
					mslabel = match[1];
				}
				match = lines[i].match('a=ssrc:' + ssrc[0] + ' label:(.+)')
				if(match) {
					label = match[1];
				}
				if(lines[i].indexOf('a=ssrc:' + ssrc_fid[0]) === 0) {
					lines.splice(i, 1); i--;
					continue;
				}
				if(lines[i].indexOf('a=ssrc:' + ssrc[0]) === 0) {
					lines.splice(i, 1); i--;
					continue;
				}
			}
			if(lines[i].length == 0) {
				lines.splice(i, 1); i--;
				continue;
			}
		}
		if(ssrc[0] < 0) {
			// Couldn't find a FID attribute, let's just take the first video SSRC we find
			insertAt = -1;
			video = false;
			for(var i=0; i<lines.length; i++) {
				var mline = lines[i].match(/m=(\w+) */);
				if(mline) {
					var medium = mline[1];
					if(medium === "video") {
						// New video m-line: make sure it's the first one
						if(ssrc[0] < 0) {
							video = true;
						} else {
							// We're done, let's add the new attributes here
							insertAt = i;
							break;
						}
					} else {
						// New non-video m-line: do we have what we were looking for?
						if(ssrc[0] > -1) {
							// We're done, let's add the new attributes here
							insertAt = i;
							break;
						}
					}
					continue;
				}
				if(!video)
					continue;
				if(ssrc[0] < 0) {
					var value = lines[i].match(/a=ssrc:(\d+)/);
					if(value) {
						ssrc[0] = value[1];
						lines.splice(i, 1); i--;
						continue;
					}
				} else {
					var match = lines[i].match('a=ssrc:' + ssrc[0] + ' cname:(.+)')
					if(match) {
						cname = match[1];
					}
					match = lines[i].match('a=ssrc:' + ssrc[0] + ' msid:(.+)')
					if(match) {
						msid = match[1];
					}
					match = lines[i].match('a=ssrc:' + ssrc[0] + ' mslabel:(.+)')
					if(match) {
						mslabel = match[1];
					}
					match = lines[i].match('a=ssrc:' + ssrc[0] + ' label:(.+)')
					if(match) {
						label = match[1];
					}
					if(lines[i].indexOf('a=ssrc:' + ssrc_fid[0]) === 0) {
						lines.splice(i, 1); i--;
						continue;
					}
					if(lines[i].indexOf('a=ssrc:' + ssrc[0]) === 0) {
						lines.splice(i, 1); i--;
						continue;
					}
				}
				if(lines[i].length === 0) {
					lines.splice(i, 1); i--;
					continue;
				}
			}
		}
		if(ssrc[0] < 0) {
			// Still nothing, let's just return the SDP we were asked to munge
			Janus.warn("Couldn't find the video SSRC, simulcasting NOT enabled");
			return sdp;
		}
		if(insertAt < 0) {
			// Append at the end
			insertAt = lines.length;
		}
		// Generate a couple of SSRCs (for retransmissions too)
		// Note: should we check if there are conflicts, here?
		ssrc[1] = Math.floor(Math.random()*0xFFFFFFFF);
		ssrc[2] = Math.floor(Math.random()*0xFFFFFFFF);
		ssrc_fid[1] = Math.floor(Math.random()*0xFFFFFFFF);
		ssrc_fid[2] = Math.floor(Math.random()*0xFFFFFFFF);
		// Add attributes to the SDP
		for(var i=0; i<ssrc.length; i++) {
			if(cname) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc[i] + ' cname:' + cname);
				insertAt++;
			}
			if(msid) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc[i] + ' msid:' + msid);
				insertAt++;
			}
			if(mslabel) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc[i] + ' mslabel:' + mslabel);
				insertAt++;
			}
			if(label) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc[i] + ' label:' + label);
				insertAt++;
			}
			// Add the same info for the retransmission SSRC
			if(cname) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc_fid[i] + ' cname:' + cname);
				insertAt++;
			}
			if(msid) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc_fid[i] + ' msid:' + msid);
				insertAt++;
			}
			if(mslabel) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc_fid[i] + ' mslabel:' + mslabel);
				insertAt++;
			}
			if(label) {
				lines.splice(insertAt, 0, 'a=ssrc:' + ssrc_fid[i] + ' label:' + label);
				insertAt++;
			}
		}
		lines.splice(insertAt, 0, 'a=ssrc-group:FID ' + ssrc[2] + ' ' + ssrc_fid[2]);
		lines.splice(insertAt, 0, 'a=ssrc-group:FID ' + ssrc[1] + ' ' + ssrc_fid[1]);
		lines.splice(insertAt, 0, 'a=ssrc-group:FID ' + ssrc[0] + ' ' + ssrc_fid[0]);
		lines.splice(insertAt, 0, 'a=ssrc-group:SIM ' + ssrc[0] + ' ' + ssrc[1] + ' ' + ssrc[2]);
		sdp = lines.join("\r\n");
		if(!sdp.endsWith("\r\n"))
			sdp += "\r\n";
		return sdp;
	}

	// Helper methods to parse a media object
	function isAudioSendEnabled(media) {
		Janus.debug("isAudioSendEnabled:", media);
		if(!media)
			return true;	// Default
		if(media.audio === false)
			return false;	// Generic audio has precedence
		if(media.audioSend === undefined || media.audioSend === null)
			return true;	// Default
		return (media.audioSend === true);
	}

	function isAudioSendRequired(media) {
		Janus.debug("isAudioSendRequired:", media);
		if(!media)
			return false;	// Default
		if(media.audio === false || media.audioSend === false)
			return false;	// If we're not asking to capture audio, it's not required
		if(media.failIfNoAudio === undefined || media.failIfNoAudio === null)
			return false;	// Default
		return (media.failIfNoAudio === true);
	}

	function isAudioRecvEnabled(media) {
		Janus.debug("isAudioRecvEnabled:", media);
		if(!media)
			return true;	// Default
		if(media.audio === false)
			return false;	// Generic audio has precedence
		if(media.audioRecv === undefined || media.audioRecv === null)
			return true;	// Default
		return (media.audioRecv === true);
	}

	function isVideoSendEnabled(media) {
		Janus.debug("isVideoSendEnabled:", media);
		if(!media)
			return true;	// Default
		if(media.video === false)
			return false;	// Generic video has precedence
		if(media.videoSend === undefined || media.videoSend === null)
			return true;	// Default
		return (media.videoSend === true);
	}

	function isVideoSendRequired(media) {
		Janus.debug("isVideoSendRequired:", media);
		if(!media)
			return false;	// Default
		if(media.video === false || media.videoSend === false)
			return false;	// If we're not asking to capture video, it's not required
		if(media.failIfNoVideo === undefined || media.failIfNoVideo === null)
			return false;	// Default
		return (media.failIfNoVideo === true);
	}

	function isVideoRecvEnabled(media) {
		Janus.debug("isVideoRecvEnabled:", media);
		if(!media)
			return true;	// Default
		if(media.video === false)
			return false;	// Generic video has precedence
		if(media.videoRecv === undefined || media.videoRecv === null)
			return true;	// Default
		return (media.videoRecv === true);
	}

	function isScreenSendEnabled(media) {
		Janus.debug("isScreenSendEnabled:", media);
		if (!media)
			return false;
		if (typeof media.video !== 'object' || typeof media.video.mandatory !== 'object')
			return false;
		var constraints = media.video.mandatory;
		if (constraints.chromeMediaSource)
			return constraints.chromeMediaSource === 'desktop' || constraints.chromeMediaSource === 'screen';
		else if (constraints.mozMediaSource)
			return constraints.mozMediaSource === 'window' || constraints.mozMediaSource === 'screen';
		else if (constraints.mediaSource)
			return constraints.mediaSource === 'window' || constraints.mediaSource === 'screen';
		return false;
	}

	function isDataEnabled(media) {
		Janus.debug("isDataEnabled:", media);
		if(Janus.webRTCAdapter.browserDetails.browser === "edge") {
			Janus.warn("Edge doesn't support data channels yet");
			return false;
		}
		if(media === undefined || media === null)
			return false;	// Default
		return (media.data === true);
	}

	function isTrickleEnabled(trickle) {
		Janus.debug("isTrickleEnabled:", trickle);
		return (trickle === false) ? false : true;
	}
}

export default Janus
