<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Publish event</h2>
    <div class="row">
      <div class="col-12 col-lg-12 col-xl-8">
        <b-form inline>
          <b-input v-model="channel" class="mr-2 mb-2 mb-lg-0" placeholder="channel"></b-input>
          <b-input v-model="event" class="mr-2 mb-2 mb-lg-0 flex-grow-0 flex-lg-grow-1" placeholder="event"></b-input>
          <ButtonJaffa @click="publish" class="mr-2 mb-2 mb-lg-0">Publish</ButtonJaffa>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa"
import publishSubscribeService from "@/store/publishSubscribeService.js"
import notificationStore from "@/store/notificationStore.js"

export default {
  name: "PublishEvent",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      channel: this.defaultChannel,
      event: '{"category": ""}',
    }
  },
  methods: {
    publish() {
      try {
        let parsedEvent = JSON.parse(this.event)
        publishSubscribeService.commit('publish', {channel: this.channel, event: parsedEvent})
      } catch {
        notificationStore.pushError(this.event + " l'événement n'est pas sérialisable en JSON")
        return
      }
    },
  },
  props: ["defaultChannel"],
}
</script>
