<template>
  <b-card
    header="New room"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <b-form class="d-flex flex-column justify-content-between h-100">
      <div>
        <div class="row mb-3">
          <div class="col-4 d-flex align-items-center">
            <label for="scenario" class="mb-0">Scenario</label>
          </div>
          <div class="col-8">
            <b-form-input
              id="scenario"
              v-model="form.scenario"
              required
              placeholder="Riddles in a hammock"
            ></b-form-input>
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-4 d-flex align-items-center">
            <label for="cardinal" class="mb-0">Cardinal</label>
          </div>
          <div class="col-8">
            <b-form-input
              id="cardinal"
              v-model="form.cardinal"
              required
              placeholder="2, (2), bis, ter..."
            ></b-form-input>
          </div>
        </div>
      </div>

      <div>
        <div class="row">
          <div class="col-12">
            <ButtonJaffa type="submit" class="btn-block">Add</ButtonJaffa>
          </div>
        </div>
      </div>
    </b-form>
  </b-card>
</template>

<script>
import ButtonJaffa from '@/components/ButtonJaffa.vue'

export default {
  name: 'PageHomeRoomCreate',
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      form: {
        scenario: "",
        cardinal: "",
      }
    }
  },
}
</script>
