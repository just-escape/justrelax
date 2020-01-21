<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Send event</h2>
    <div class="row">
      <div class="col-12 col-lg-12 col-xl-8">
        <b-form inline>
          <b-input v-model="node" class="mr-2 mb-2 mb-lg-0" placeholder="node"></b-input>
          <b-input v-model="event" class="mr-2 mb-2 mb-lg-0 flex-grow-0 flex-lg-grow-1" placeholder="event"></b-input>
          <ButtonJaffa @click="sendTo" class="mr-2 mb-2 mb-lg-0">Send to</ButtonJaffa>
          <ButtonJaffa @click="sendAs" class="mb-2 mb-lg-0">Send as</ButtonJaffa>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa"
import roomStore from "@/store/roomStore.js"

export default {
  name: "SendMessage",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      node: "",
      event: "",
    }
  },
  methods: {
    sendTo: function() {
      let roomId = this.room.id
      let node = this.node
      let event = this.event
      roomStore.dispatch('processSendEventTo', {roomId, node, event})
    },
    sendAs: function() {
      let roomId = this.room.id
      let node = this.node
      let event = this.event
      roomStore.dispatch('processSendEventAs', {roomId, node, event})
    },
  },
  props: ["room"]
}
</script>
