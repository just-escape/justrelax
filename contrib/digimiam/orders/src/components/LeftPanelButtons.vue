<template>
  <div class="text-right">
    <div class="d-flex flex-row justify-content-between">
      <div class="align-self-end">
        <b-btn-group>
          <b-btn variant="info" size="md">
            Français
          </b-btn>
          <b-btn variant="info" size="md">
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
export default {
  name: "LeftPanelButtons"
}
</script>
