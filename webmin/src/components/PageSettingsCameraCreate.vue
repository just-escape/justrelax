<template>
  <div class="row">
    <div class="col-2 d-flex align-items-center pr-0">
      <b-img
        :src="url"
        class="img-fluid border-deepdark"
        :blank="url == ''"
        blank-color="#3c3c3e"
      />
    </div>
    <div class="col-4">
      <b-form>
        <div class="row mb-3">
          <div class="col-3 align-items-center d-flex">
            <label for="name" class="mb-0">Name</label>
          </div>
          <div class="col-9">
            <b-form-input
              id="name"
              v-model="name"
              required
            ></b-form-input>
          </div>
        </div>

        <div class="row">
          <div class="col-3 align-items-center d-flex">
            <label for="url" class="mb-0">URL</label>
          </div>
          <div class="col-9">
            <b-form-input
              id="url"
              v-model="url"
              required
              placeholder="https://..."
            ></b-form-input>
          </div>
        </div>
      </b-form>
    </div>

    <div class="col-2 d-flex align-items-center justify-content-end">
      <ButtonJaffa>
        <i class="fas fa-plus"></i>
      </ButtonJaffa>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from '@/components/ButtonJaffa.vue'

export default {
  name: 'PageSettingsCameraCreate.vue',
  components: {
    ButtonJaffa
  },
  data: function() {
    return {
      name: 'Cam ' + (this.nCameras + 1),
      url: '',
    }
  },
  watch: {
    nCameras: function(newValue, oldValue) {
      if (this.name == 'Cam ' + (oldValue + 1)) {
        this.name = 'Cam ' + (newValue + 1)
      }
    }
  },
  props: ["nCameras"]
}
</script>
