<template>
  <div class="text-right">
    <div class="d-flex flex-row justify-content-between">
      <div class="align-self-end">
        <b-btn-group>
          <UnclickableButton>
            <img class="lang" src="@/assets/lang.svg">
          </UnclickableButton>
          <b-btn variant="info">
            Français
          </b-btn>
          <b-btn variant="info">
            English
          </b-btn>
        </b-btn-group>
      </div>
      <div>
        <b-btn variant="outline-primary" size="lg">
          Reset order
        </b-btn>
      </div>
    </div>
  </div>
</template>

<script>
import UnclickableButton from "@/components/UnclickableButton.vue"

export default {
  name: "LeftPanelButtons",
  components: {
    UnclickableButton,
  },
}
</script>

<style scoped>
.lang {
  height: 20px;
  width: auto;
}
</style>
