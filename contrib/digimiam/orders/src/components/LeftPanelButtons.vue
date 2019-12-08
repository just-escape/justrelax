<template>
  <div class="text-right">
    <div class="d-flex flex-row justify-content-between">
      <div class="align-self-end">
        <b-btn-group>
          <UnclickableDarkButton>
            <img class="lang" src="@/assets/lang.svg">
          </UnclickableDarkButton>
          <b-btn @click="setLocale('fr')" variant="info">
            Français
          </b-btn>
          <b-btn @click="setLocale('en')" variant="info">
            English
          </b-btn>
        </b-btn-group>
      </div>
      <div>
        <b-btn @click="resetOrder" variant="outline-primary" size="lg">
          Reset order
        </b-btn>
      </div>
    </div>
  </div>
</template>

<script>
import UnclickableDarkButton from "@/components/UnclickableDarkButton.vue"
import orderStore from '@/store/orderStore.js'
import router from '@/router.js'
import i18n from '@/locales.js'

export default {
  name: "LeftPanelButtons",
  components: {
    UnclickableDarkButton,
  },
  methods: {
    setLocale: function(lang) {
      router.push({path: '/', query: {'lang': lang}})
      i18n.locale = lang
    },
    resetOrder: function() {
      orderStore.commit('resetOrder')
    },
  },
}
</script>

<style scoped>
.lang {
  height: 20px;
  width: auto;
}
</style>
