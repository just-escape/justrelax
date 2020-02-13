<template>
  <div class="text-right p-3">
    <select v-model="$i18n.locale">
      <option
        v-for="l in availableLocales"
        :key="l.value"
        :value="l.value"
      >
        {{ l.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "LocaleSelector",
  data() {
    return {
      locale: "en",
      availableLocales: [
        {
          "value": "en",
          "label": "EN",
        },
        {
          "value": "fr",
          "label": "FR",
        },
      ]
    }
  },
}
</script>