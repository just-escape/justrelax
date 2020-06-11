<template>
  <Window :title="$t('CONFIGURATION')" class="h-100">
    <div class="d-flex h-100">
      <div class="d-flex flex-column lh-1 mx-4 justify-content-center h-100 w-100">
        <div class="d-flex flex-row mb-5">
            <div>Mode</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">Marmitron</span> / manuel</div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>Sécurité</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>activée / <span class="opacity-25">désactivée</span></div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>Maintenance en cours</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>oui / <span class="opacity-25">non</span></div>
        </div>
        <div class="d-flex flex-row mb-5">
            <div>Ouverture public</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">oui</span> / non</div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>Approvisionnement</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>Marmitron / <span class="opacity-25">manuel</span></div>
        </div>
        <div class="d-flex flex-row mb-3">
            <div>Hydrogonflage des aliments</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div>oui / <span class="opacity-25">non</span></div>
        </div>
        <div class="d-flex flex-row">
            <div>Qualité de l'air</div>
            <span class="underline-dots flex-grow-1 mx-1"></span>
            <div><span class="opacity-25">optimale</span> / économique</div>
        </div>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'

export default {
  name: "ConfigurationWindow",
  components: {
    Window,
  }
}
</script>

<style scoped>
.underline-dots {
  font-size: 18px;
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}

.opacity-25 {
  opacity: 0.25;
}
</style>