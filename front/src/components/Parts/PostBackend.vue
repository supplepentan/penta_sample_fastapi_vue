<script setup lang="ts">
import axios, { AxiosResponse } from "axios";
import { ref } from "vue";

interface Props {
    backendUrl: string
}

const props = defineProps<Props>();
const file = ref();
const previewImage = ref();

const fileSelected = (event: any): void => {
    file.value = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        previewImage.value = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
};
const fileUpload = (): void => {
    console.log(props.backendUrl);
    const formData = new FormData();
    formData.append("file", file.value);
    axios
        .post(props.backendUrl, formData, {
            responseType: "blob",
        })
        .then((response: AxiosResponse<any, any>) => {
            let mineType: string | undefined = response.headers["content-type"];
            if (mineType === "image/jpeg" | mineType === "image/png") {
                console.log(response.headers["content-type"]);
                const blob = new Blob([response.data], { type: mineType });
                let url: string = URL.createObjectURL(blob);
                const a: HTMLAnchorElement = document.createElement("a");
                document.body.appendChild(a);
                a.download = "returnFile.".concat(mineType.slice(-3));
                a.href = url;
                a.click();
            }
        })
        .catch(error => console.log(error));
};
</script>
<template>
    <div>
        <div class="p-2">
            <label
                class="px-4 py-2 bg-transparent border-blue-500 rounded cursor-pointer bg-sky-200 ring-2 hover:bg-blue-300 hover:text-white hover:border-transparent">
                Select File !
                <input class="hidden" type="file" v-on:change="fileSelected" />
            </label>
            <button v-on:click="fileUpload"
                class="px-4 py-2 font-semibold text-blue-700 bg-transparent bg-blue-100 border-blue-500 rounded ring-2 hover:bg-blue-300 hover:text-white hover:border-transparent">
                Make It !
            </button>
        </div>
        <div class="grid grid-cols-2">
            <div>
                <img v-bind:src="previewImage" class="img-fluid" alt="" />
            </div>
            <div v-if="file" class="m-2 p-2 border rounded-lg border-slate-400">
                <p>Name: {{file.name}}</p>
                <p>Size: {{file.size}}</p>
                <p>Type: {{file.type}}</p>
            </div>
        </div>
    </div>
</template>