<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Send message</h2>
    <div class="row">
      <div class="col-12 col-lg-12 col-xl-8">
        <b-form inline>
          <b-input v-model="to" class="mr-2 mb-2 mb-lg-0" placeholder="to"></b-input>
          <b-input v-model="content" class="mr-2 mb-2 mb-lg-0 flex-grow-0 flex-lg-grow-1" placeholder="content"></b-input>
          <b-form-checkbox v-model="json" class="mr-4 mb-2 mb-lg-0">JSON</b-form-checkbox>
          <ButtonJaffa @click="send" class="mb-2 mb-lg-0">Send</ButtonJaffa>
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
      to: "",
      content: "",
      json: false,
    }
  },
  methods: {
    send: function() {
      let roomId = this.room.id
      let to = this.to
      let content = this.content
      let json = this.json
      roomStore.dispatch('processSendMessage', {roomId, to, content, json})
    }
  },
  props: ["room"]
}
</script>
